from bioage_framework.chat_model import ChatModel
from sklearn.metrics import mean_absolute_error
import pandas as pd
import torch
import shap
import numpy as np

class Connector:
    def __init__(self, bioage_model: object, chat_model: ChatModel):
        self.bioage_model = bioage_model
        self.chat_model = chat_model

    def inference(self, data: pd.DataFrame):
        self.bioage_model.eval()
        self.bioage_model.freeze()
        return self.bioage_model(torch.from_numpy(data.drop('Age', axis=1).values)).cpu().detach().numpy().ravel()

    def analyze(self, data: pd.DataFrame, **kwargs):
        answer = ''
        data['bio_age'] = self.inference(data)
        acceleration = data['bio_age'].values - data['Age'].values

        answer += 'You biological age is {age}, and you aging acceleration is {acceleration}, which means '.format(age=round(data['bio_age'].values[0]), acceleration=round(acceleration[0]))

        if (acceleration > 1):
            answer += 'you are ageing quicker than normal.\n\n'
        elif (acceleration > -1 and acceleration < 1):
            answer += 'you are ageing normally.\n\n'
        else:
            answer += 'you are ageing slower than normal.\n\n'

        answer += 'Here is some more information about your data. \n\n'

        shap_dict = kwargs.get('shap_dict', None)

        if shap_dict == None:
            return
        
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
            answer += f'{feats[i]}: {values[i]}\n'
            if values[i] > 0:
                level = 'an increased'
            else:
                level = 'a reduced'
            prompt = f'What does {level} level of {feats[i]} mean?'
            answer += self.chat_model.query(prompt=prompt)[1]
            answer += '\n\n'
        return answer

