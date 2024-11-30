from sklearn.metrics import mean_absolute_error
import pandas as pd
import shap
import torch
import numpy as np

from llamba.chatmodels.chat_model import AbstractChatModel
from llamba.bioage_model import BioAgeModel
from llamba.plots import kde_plot

class LlambaConnector:
    def __init__(self, bioage_model: BioAgeModel, chat_model: AbstractChatModel):
        self.bioage_model = bioage_model
        self.chat_model = chat_model

    def analyze(self, data: pd.DataFrame, device=torch.device('cpu'), **kwargs):
        answer = ''
        data['bio_age'] = self.bioage_model.inference(data=data.drop(['Age'], axis=1), device=device)
        acceleration = data['bio_age'].values - data['Age'].values
        answer += 'Your bioage is {bio_age} and your aging acceleration is {acceleration}, which means ' \
            .format(bio_age=round(data['bio_age'].values[0]), 
                    acceleration=round(acceleration[0]))

        if (acceleration > 1):
            answer += 'you are ageing quicker than normal.\n\n'
        elif (acceleration > -1 and acceleration < 1):
            answer += 'you are ageing normally.\n\n'
        else:
            answer += 'you are ageing slower than normal.\n\n'

        shap_dict = kwargs.get('shap_dict', None)

        if shap_dict == None:
            return {"analysis": answer, "acceleration": acceleration[0]}
        
        answer += 'Here is some more information about your data. \n\n'
        
        explainer = shap_dict['explainer']

        feats = data.drop(['Age', 'bio_age'], axis=1).columns.to_list()
        shap_values_trgt = explainer.shap_values(data.loc[0, feats].values)
        base_value = explainer.expected_value[0]

        explanation = shap.Explanation(
            values=shap_values_trgt,
            base_values=base_value,
            data=data.loc[0, feats].values,
            feature_names=feats)

        permutation = np.array(explanation.values).argsort()
        
        # Top-2 values
        n = 2
        values = np.flip(np.array(explanation.values)[permutation])[:n]
        data = np.flip(np.array(explanation.data)[permutation])[:n]
        feats = np.flip(np.array(feats)[permutation])[:n]

        for i in range(n):
            answer += f'{feats[i]}: {data[i]}\n'
            if values[i] > 0:
                level = 'an increased'
            else:
                level = 'a reduced'
            prompt = f'What is {feats[i]}? What does {level} level of {feats[i]} mean?'
            res = self.chat_model.query(prompt=prompt)[1]
            answer += res
            answer += '\n\n'

        return {"analysis": answer, "acceleration": acceleration[0], "features": feats}

