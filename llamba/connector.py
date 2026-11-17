import pandas as pd

from llamba.chatmodels.chat_model import BaseChatModel
from llamba.util.clock import Clock
from llamba.util.condition import Condition
from llamba.util.document_repo import DocumentRepoQdrant
from llamba.util.module_coordinator import ModuleCoordinator
from llamba.util.module import Module
from llamba.util.strings.language_manager import Lang, set_language, get_string

class LlambaConnector:
    def __init__(self, chat_model: BaseChatModel, **kwargs):
        self.module_coordinator = ModuleCoordinator()
        self.chat_model = chat_model
        self.clock = ""
        self.condition = ""
        self.language = kwargs.get('language', "ru")
        set_language(Lang.EN if self.language == 'en' else Lang.RU)
        self.document_repo = None

    def specify_clock_name(self, name: str, doi: str):
        self.clock = Clock(name, doi)
    
    def specify_db(self, document_repo: DocumentRepoQdrant):
        self.document_repo = document_repo

    def specify_conditions(self, condition: str, duration: str):
        self.condition = Condition(condition, duration)

    def add_module(self, module: Module):
        self.module_coordinator.add_module(module=module, 
                                           chat_model=self.chat_model,
                                           language=self.language)

    # Analysis
    def analyze(self, data: pd.DataFrame, **kwargs):
        self.analysis = self.module_coordinator.analyze(data=data, 
                                                        clock=self.clock, 
                                                        document_repo=self.document_repo,
                                                        condition=self.condition, 
                                                        **kwargs)
        formatted_analysis = self.format_answer()
        return {'analysis': formatted_analysis}
    
    # Finalization
    def format_answer(self):
        format_prompt = get_string("format_prompt", analysis=self.analysis)
        formatted_answer = self.query_prompt(format_prompt)
        return formatted_answer

    def query_prompt(self, prompt: str):
        res = self.chat_model.query(prompt=prompt)[1]
        return res

    # Prompt generation
    def produce_recommendations_prompt(self):
            prompt = get_string("recommendations_1")
            if self.condition:
                prompt += get_string("recommendations_2", condition_name=self.condition.name, condition_duration=self.condition.duration)
            prompt += get_string("recommendations_3", analysis=self.analysis)
            return prompt

    # Finalization
    def produce_recommendations(self):
        rec_prompt = self.produce_recommendations_prompt()
        answer = self.query_prompt(rec_prompt)
        return answer