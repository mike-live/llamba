import requests as rq
from http import HTTPStatus

class AbstractChatModel:
    def __init__(self): 
        self.url = ""

    def get_system_message(self):
        return 'I want you to act a gerontology expert. Answer prompts shortly, without emotions and greetings, and in the same language they are asked.'

    def prepare_query(self, prompt):
        data_input = {
            "messages": self.get_system_message() + [{'role': 'user', 'content': f'{prompt}'}]
        }
        self.data_input = data_input

    def query(self, prompt: str):
        self.prepare_query(prompt)
        num_tries = 3
        try:
            for _ in range(num_tries):
                response = rq.post(self.url, 
                                   json=self.data_input,
                                   timeout=30)
                response.raise_for_status()
                if response.status_code != HTTPStatus.METHOD_NOT_ALLOWED:
                    break
        except Exception as e:
            print(e)
            return False, "Incorrect bot configuration."
        
        try:
            data = response.json()
            if response.status_code != HTTPStatus.OK:
                return False, f"Error:{response.status_code} ({data['done_reason']})"
            bot_answer = data['response']
            return True, bot_answer
        except rq.exceptions.JSONDecodeError as e:
            print(f"JSON decode error. Error:{response.status_code}")
            print('Input data:')
            print(self.data_input)
            print(response.text)
            return False, f"JSON decode error. Error:{response.status_code}"