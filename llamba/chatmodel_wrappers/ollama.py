import json
import requests as rq

from llamba.chat_model import AbstractChatModel

class OllamaModel(AbstractChatModel):
    def __init__(self, model: str, url="http://127.0.0.1:11434/api/generate"):
        super(OllamaModel, self).__init__()
        self.url = url
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

    def prepare_query(self, prompt: str, kwargs):
        data_input = {
            "model": self.model,
            "prompt": prompt,
            "system": self.get_system_message(),
            "stream": False
        }
        for parameter in kwargs:
            data_input[parameter] = kwargs.get(parameter, None)
        self.data_input = data_input

    def query(self, prompt: str,
              **kwargs):
        self.prepare_query(prompt, kwargs)
        num_tries = 3
        try:
            for _ in range(num_tries):
                response = rq.post(self.url, 
                                   json=self.data_input,
                                   timeout=30)
                response.raise_for_status()
                if response.status_code != 405:
                    break
        except Exception as e:
            print(e)
            return False, "Incorrect bot configuration."
        
        try:
            data = response.json()
            if response.status_code != 200:
                return False, f"Error:{response.status_code} ({data['done_reason']})"
            bot_answer = data['response']
            return True, bot_answer
        except rq.exceptions.JSONDecodeError as e:
            print(f"JSON decode error. Error:{response.status_code}")
            print('Input data:')
            print(self.data_input)
            print(response.text)
            return False, f"JSON decode error. Error:{response.status_code}"