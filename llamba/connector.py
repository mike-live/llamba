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
        top_n = kwargs.get('top_n', None)
        if shap_dict == None or top_n == None:
            return {"analysis": self.answer, "acceleration": acceleration[0]}
        
        self.answer += 'Here is some more information about your data. \n\n'
        
        feats = data.drop(['Age', 'bio_age'], axis=1).columns.to_list()
        top_shap = self.bioage_model.get_top_shap(top_n, data, feats, shap_dict)
        
        self.generate_prompts(top_n=top_n, data=top_shap['data'], feats=top_shap['feats'], values=top_shap['values'])
        self.query_prompts()

        return {"analysis": self.answer, "acceleration": acceleration[0], "features": feats}    

    def generate_prompts(self, top_n, data, feats, values):
        for i in range(top_n):
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