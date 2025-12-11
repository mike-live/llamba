import pandas as pd
import torch
from typing import Callable

from llamba.chatmodels.chat_model import AbstractChatModel
from llamba.util.disease import Disease
from llamba_library.bioage_model import BioAgeModel
from llamba.util.disease import inflammatory_disease_list
from llamba.util.clock import Clock
from llamba.util.document_repo import DocumentRepoQdrant

class LlambaConnector:
    def __init__(self, bioage_model: BioAgeModel, chat_model: AbstractChatModel, **kwargs):
        self.bioage_model = bioage_model
        self.chat_model = chat_model
        self.answer = ""
        self.clock = ""
        self.language = kwargs.get('language', "en")
        self.document_repo = None

    def specify_clock_name(self, name: str, doi: str):
        self.clock = Clock(name, doi)
    
    def specify_db(self, document_repo: DocumentRepoQdrant):
        self.document_repo = document_repo

    # Prompt creation
    def produce_feat_analysis_prompts(self, top_n, data, feats, values):
        prompts = []
        for i in range(top_n):
            self.answer += f'{feats[i]}: {data[i]}\n'
            if values[i] > 0:
                level = 'an increased'
            else:
                level = 'a reduced'
            prompts.append(f'What is {feats[i]}? What does {level} level of {feats[i]} mean?')
        return prompts    

    def produce_risk_prompts(self):
        disease_list = inflammatory_disease_list(lang=self.language)
        risk_prompts = []
        for disease in disease_list:
            risk_prompts.append(self.produce_risk_prompt(disease=disease))
        return risk_prompts

    def produce_risk_prompt(self, disease: Disease):
        disease_prompt = ""

        disease_prompt += f"Given the following parameters, estimate the risk of {disease.short_name} (ICD: {disease.icd}) occurring: "
        for i in range(self.top_n):
            disease_prompt += "{param}: {value}, acceleration: {acc}\n".format(param=self.top_shap['feats'][i], value=self.top_shap['data'][i], acc=self.top_shap['values'][i])
            
        return disease_prompt
    
    def produce_recommendations_prompt(self):
        return f"Given the analysis results that will follow, what would you recommend to normalize the results and lower the chance of disease occurrence? Explain each recommendation in detail. \n The analysis: {self.answer}"
    
    # Answer construction
    def produce_basic_answer(self):
        answer = 'Your bioage is {bio_age} and your aging acceleration is {acceleration}, which means ' \
            .format(bio_age=round(self.bio_age), 
                    acceleration=round(self.acceleration[0]))

        if (self.acceleration > 1):
            answer += 'you are ageing quicker than normal.\n\n'
        elif (self.acceleration > -1 and self.acceleration < 1):
            answer += 'you are ageing normally.\n\n'
        else:
            answer += 'you are ageing slower than normal.\n\n'
        return answer

    def produce_advanced_answer(self):
        answer = 'Here is some more information about your data. \n\n'
        answer += self.query_prompts(self.feat_prompts)
        return answer
    
    def produce_risk_answer(self):
        answer = 'How likely you are to get the following inflammatory diseases. \n\n'
        answer += self.query_prompts(self.risk_prompts)
        return answer
    
    # Analysis
    def advanced_analysis(self, data: pd.DataFrame, train_data: pd.DataFrame, predict_func: Callable):
        feats = data.drop(['Age', 'bio_age'], axis=1).columns.to_list()
        self.top_shap = self.bioage_model.get_top_shap(self.top_n, data, feats, train_data, predict_func)
        self.feat_prompts = self.produce_feat_analysis_prompts(top_n=self.top_n, data=self.top_shap['data'], feats=self.top_shap['feats'], values=self.top_shap['values'])
        return {"analysis": self.answer, "acceleration": self.acceleration[0], "features": feats}   
    
    def risk_analysis(self):
        self.risk_prompts = self.produce_risk_prompts()
        return
    
    # Finalization
    def produce_recommendations(self):
        rec_prompt = self.produce_recommendations_prompt()
        answer = self.query_prompt(rec_prompt)
        return answer
    
    def format_answer(self):
        format_prompt = f"You are given a data report. Make sure that it is in {self.language}. Structure it in the following way: " \
        "1) Show bioage and age acceleration." \
        "2) List the most influential parameters and their values as a table with the Feature, Value, Age acceleration columns." \
        "3) Give a short description for each most influential parameter and what it means if the value is greater/smaller than normal." \
        "4) Provide information about the risk of disease occurrence as a table with the Disease, Risk, Comments columns." \
        "5) Describe in detail how each disease is associated with parameters." \
        "" \
        "The report is as follows: {answer}".format(answer=self.answer)
        formatted_answer = self.query_prompt(format_prompt)
        return formatted_answer

    def analyze(self, data: pd.DataFrame, device=torch.device('cpu'), analyze_feats=False, analyze_risks=False, **kwargs):
        self._analyze_feats = analyze_feats
        self._analyze_risks = analyze_risks
        
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

        formatted_answer = self.format_answer()

        return {"analysis": formatted_answer, "acceleration": self.acceleration[0]}
    
    # Prompt querying
    def query_prompt(self, prompt: str):
        if self.document_repo:
            try:
                context = self.document_repo.search(prompt)
                prompt += f"Use the following information as context: {context}"
            except:
                pass
        if self.clock:
            clock_prompt = f"Use {self.clock.name} (DOI: {self.clock.doi}) for a reference as an immunological clock. "
            prompt = clock_prompt + prompt
        res = self.chat_model.query(prompt=prompt)[1]
        return res

    def query_prompts(self, prompts: list):
        answer = ""
        for prompt in prompts:
            res = self.query_prompt(prompt)
            answer += res
            answer += '\n\n'
        return answer