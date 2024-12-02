from sklearn.metrics import mean_absolute_error
import pandas as pd
import shap
import torch
import numpy as np

from llamba.chatmodels.chat_model import AbstractChatModel
from llamba_library.bioage_model import BioAgeModel
from llamba_library.plots import kde_plot

class LlambaConnector:
    def __init__(self, bioage_model: BioAgeModel, chat_model: AbstractChatModel):
        self.bioage_model = bioage_model
        self.chat_model = chat_model
        self.answer = ""
        self.prompts = []

    def analyze(self, data: pd.DataFrame, device=torch.device('cpu'), **kwargs):
        data['bio_age'] = self.bioage_model.inference(data=data.drop(['Age'], axis=1), device=device)
        acceleration = data['bio_age'].values - data['Age'].values
        self.answer += 'Your bioage is {bio_age} and your aging acceleration is {acceleration}, which means ' \
            .format(bio_age=round(data['bio_age'].values[0]), 
                    acceleration=round(acceleration[0]))

        if (acceleration > 1):
            self.answer += 'you are ageing quicker than normal.\n\n'
        elif (acceleration > -1 and acceleration < 1):
            self.answer += 'you are ageing normally.\n\n'
        else:
            self.answer += 'you are ageing slower than normal.\n\n'

        shap_dict = kwargs.get('shap_dict', None)

        if shap_dict == None:
            return {"analysis": self.answer, "acceleration": acceleration[0]}
        
        self.answer += 'Here is some more information about your data. \n\n'
        
        explainer = shap_dict['explainer']

        feats = data.drop(['Age', 'bio_age'], axis=1).columns.to_list()
        
        self.generate_prompts(n=2, data=data, feats=feats, explainer=explainer)
        self.query_prompts()

        return {"analysis": self.answer, "acceleration": acceleration[0], "features": feats}    

    def generate_prompts(self, data, n, feats, explainer):
        shap_values_trgt = explainer.shap_values(data.loc[0, feats].values)
        base_value = explainer.expected_value[0]

        explanation = shap.Explanation(
            values=shap_values_trgt,
            base_values=base_value,
            data=data.loc[0, feats].values,
            feature_names=feats)

        permutation = np.array(explanation.values).argsort()
        
        # Top-n values
        values = np.flip(np.array(explanation.values)[permutation])[:n]
        data = np.flip(np.array(explanation.data)[permutation])[:n]
        feats = np.flip(np.array(feats)[permutation])[:n]

        for i in range(n):
            self.answer += f'{feats[i]}: {data[i]}\n'
            if values[i] > 0:
                level = 'an increased'
            else:
                level = 'a reduced'
            self.prompts.append(f'What is {feats[i]}? What does {level} level of {feats[i]} mean?')
        return self.prompts

    def query_prompts(self):
        for prompt in self.prompts:
            res = self.chat_model.query(prompt=prompt)[1]
            self.answer += res
            self.answer += '\n\n'
        return self.answer