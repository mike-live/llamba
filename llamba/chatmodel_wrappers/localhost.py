import json
import requests as rq
import subprocess

from llamba.chat_model import BaseModel

class OllamaModel(BaseModel):
    def __init__(self, model: str, url="localhost:11434"):
        super(OllamaModel, self).__init__()
        self.url = url
        self.model = model

    def check_connection(self):
        connection = subprocess.run(["curl", f"{self.url}"], capture_output=True)
        if connection.stdout != "Ollama is running":
            return False
        return True

    def prepare_query(self, prompt: str, suffix: str, kwargs):
        data_input = {
            "model": self.model,
            "prompt": prompt,
            "suffix": suffix,
            "format": "json",
        }
        for parameter in kwargs:
            data_input[parameter] = kwargs.get(parameter, None)
        self.data_input = data_input

    def query(self, prompt: str, 
              suffix: str, 
              **kwargs):
        kwargs['system'] = self.get_system_message()
        self.prepare_query(prompt, suffix, kwargs)
        #data_input_json = json.dumps(self.data_input).encode('utf-8')
        
        num_tries = 3

        try:
            for _ in range(num_tries):
                response = rq.post(self.url + '/api/generate', json=self.data_input, stream=False)
                response.raise_for_status()
                if response.status_code != 405:
                    break
        except:
            return False, "Incorrect bot configuration."

        try:
            data = response.json()
            if response.status_code != 200:
                return False, f"Error:{response.status_code}({data['done']})"
            bot_answer = data['response']
            return True, bot_answer
        except rq.exceptions.JSONDecodeError as e:
            print(f"JSON decode error. Error:{response.status_code}")
            print('Input data:')
            print(self.data_input)
            print(response.text)
            return False, f"JSON decode error. Error:{response.status_code}"