import requests as rq
from http import HTTPStatus
from .base_config import *

class BaseChatModel:
    def __init__(self): 
        self.url = ""
        self.headers = {}
        self._system_prompt = system_prompt

    @property
    def system_prompt(self):
        return self._system_prompt

    def prepare_query(self, prompt):
        data_input = {
            "messages": [{'role': 'system', 
                          'content': self.system_prompt}] + [{'role': 'user', 'content': f'{prompt}'}]
        }
        self.data_input = data_input
    
    def handle_response(self): pass

    def query(self, prompt: str, timeout: int = 60):
        self.prepare_query(prompt)
        num_tries = 3
        try:
            for _ in range(num_tries):
                self.response = rq.post(self.url, 
                                   json=self.data_input,
                                   headers=self.headers,
                                   timeout=timeout)
                self.response.raise_for_status()
                if self.response.status_code != HTTPStatus.METHOD_NOT_ALLOWED:
                    break
        except Exception as e:
            print(e)
            return False, "Incorrect bot configuration."
        return self.handle_response()