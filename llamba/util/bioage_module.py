from llamba.util.module import Module
from llamba.util.disease import Disease
from llamba.util.disease import inflammatory_disease_list
from llamba.util.strings.language_manager import get_string

from llamba_library.bioage_model import BioAgeModel
import pandas as pd
import torch
from typing import Callable

class BioAgeModule(Module):
    def __init__(self, model: BioAgeModel, **kwargs):
        super().__init__(**kwargs)
        self.name = 'bioage'
        self.bioage_model = model

    def analyze(self, data: pd.DataFrame, **kwargs):
            analyze_feats = kwargs.get('analyze_feats', False)
            analyze_risks = kwargs.get('analyze_risks', False)

            device = kwargs.get('device', 'cpu')

            data['bio_age'] = self.bioage_model.inference(data=data.drop(['Age'], axis=1), device=device)
            self.bio_age = data['bio_age'].values[0]
            self.acceleration = data['bio_age'].values - data['Age'].values
            
            self.top_n = kwargs.get('top_n', None)
            train_data = kwargs.get('train_data', None)
            predict_func = kwargs.get('predict_func', None)
    
            self.answer += self.produce_basic_answer()
            # If we want to get info about features like what they mean and what their increased/decreased levels mean
            if analyze_feats:
                if not train_data.empty and self.top_n and predict_func != None:
                    self.advanced_analysis(data, train_data, predict_func)
                    self.answer += self.produce_advanced_answer()
                    if analyze_risks:
                        self.risk_analysis()
                        self.answer += self.produce_risk_answer()
    
            return {"analysis": self.answer, "acceleration": self.acceleration[0]}

    # Prompt creation
    def produce_feat_analysis_prompts(self, top_n, data, feats, values):
        prompts = []
        for i in range(top_n):
            self.answer += f'{feats[i]}: {data[i]}\n'
            if values[i] > 0:
                level = get_string("increased")
            else:
                level = get_string("reduced")
            prompts.append(get_string("feature_analysis_prompt", feature=feats[i], level=level))
        return prompts     
      
    def produce_risk_prompt(self, disease: Disease):
            disease_prompt = ""
            disease_prompt += get_string("disease_risk_prompt_1", disease_short_name=disease.short_name, disease_icd=disease.icd)
            for i in range(self.top_n):
                disease_prompt += get_string("disease_risk_prompt_2", param=self.top_shap['feats'][i], value=self.top_shap['data'][i], acc=self.top_shap['values'][i])
                
            return disease_prompt

    def produce_risk_prompts(self):
        disease_list = inflammatory_disease_list(lang=self.language)
        risk_prompts = []
        for disease in disease_list:
            risk_prompts.append(self.produce_risk_prompt(disease=disease))
        return risk_prompts

    # Answer construction
    def produce_basic_answer(self):
        answer = get_string("basic_answer_1", bio_age=round(self.bio_age), acceleration=round(self.acceleration[0]))

        if (self.acceleration > 1):
            answer += get_string("ageing_quicker")
        elif (self.acceleration > -1 and self.acceleration < 1):
            answer += get_string("ageing_normally")
        else:
            answer += get_string("ageing_slower")
        return answer

    def advanced_analysis(self, data: pd.DataFrame, train_data: pd.DataFrame, predict_func: Callable):
                feats = data.drop(['Age', 'bio_age'], axis=1).columns.to_list()
                self.top_shap = self.bioage_model.get_top_shap(self.top_n, data.drop(['bio_age'], axis=1), feats, train_data, predict_func)
                self.feat_prompts = self.produce_feat_analysis_prompts(top_n=self.top_n, data=self.top_shap['data'], feats=self.top_shap['feats'], values=self.top_shap['values'])
                return {"analysis": self.answer, "acceleration": self.acceleration[0], "features": feats}  

    def produce_advanced_answer(self):
        answer = get_string("more_info")
        answer += self.query_prompts(self.feat_prompts)
        return answer
    
    def produce_risk_answer(self):
        answer = get_string("inflammatory_risk")
        answer += self.query_prompts(self.risk_prompts)
        return answer

    def risk_analysis(self):
            self.risk_prompts = self.produce_risk_prompts()
            return