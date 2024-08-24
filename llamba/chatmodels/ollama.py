import json
import requests as rq

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