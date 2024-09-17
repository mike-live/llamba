import requests as rq
from http import HTTPStatus

from llamba.chat_model import AbstractChatModel

class OllamaModel(AbstractChatModel):
    def __init__(self, model: str, url="http://127.0.0.1:11434/", endpoint="api/generate"):
        super(OllamaModel, self).__init__()
        self.url = url + endpoint
        self.model = model

    def check_connection(self):
        r = rq.post(
            self.url,
            json={"model": self.model},
        )
        r.raise_for_status()
        data = r.json()
        if data['done'] != True:
            return False
        return True

    def prepare_query(self, prompt: str):
        data_input = {
            "model": self.model,
            "prompt": prompt,
            "system": self.get_system_message(),
            "stream": False
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