import requests as rq
from http import HTTPStatus

from .chat_model import AbstractChatModel

class OllamaModel(AbstractChatModel):
    def __init__(self, model: str, url="http://127.0.0.1:11434/", endpoint="api/generate", 
                 num_threads=1, check_connection_timeout=60, request_timeout=60):
        super(OllamaModel, self).__init__()
        self.url = url + endpoint
        self.model = model
        self.num_threads = num_threads
        self.check_connection_timeout = check_connection_timeout
        self.request_timeout = request_timeout

    def check_connection(self):
        r = rq.post(
            self.url,
            json={"model": self.model},
            timeout=self.check_connection_timeout
        )
        r.raise_for_status()
        data = r.json()
        if data['done'] != True:
            return False
        return True
    
    def query(self, prompt: str):
        return super().query(prompt, self.request_timeout)

    def prepare_query(self, prompt: str):
        data_input = {
            "model": self.model,
            "prompt": prompt,
            "system": self.get_system_message(),
            "stream": False,
            "options": {
                "num_threads": self.num_threads
            }   
        }
        self.data_input = data_input
    
    def handle_response(self):        
        try:
            data = self.response.json()
            if self.response.status_code != HTTPStatus.OK:
                return False, f"Error:{self.response.status_code} ({data['done_reason']})"
            bot_answer = data['response']
            return True, bot_answer
        except rq.exceptions.JSONDecodeError as e:
            print(f"JSON decode error. Error:{self.response.status_code}")
            print('Input data:')
            print(self.data_input)
            print(self.response.text)
            return False, f"JSON decode error. Error:{self.response.status_code}"