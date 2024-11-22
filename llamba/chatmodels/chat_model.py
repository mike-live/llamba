import requests as rq
from http import HTTPStatus

class AbstractChatModel:
    def __init__(self): 
        self.url = ""
        self.headers = {}

    def get_system_message(self):
        return 'I want you to act a gerontology expert. Answer prompts shortly, without emotions and greetings, and in the same language they are asked.'

    def prepare_query(self, prompt):
        data_input = {
            "messages": self.get_system_message() + [{'role': 'user', 'content': f'{prompt}'}]
        }
        self.data_input = data_input
    
    def handle_response(self): pass

    def query(self, prompt: str, timeout=60):
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