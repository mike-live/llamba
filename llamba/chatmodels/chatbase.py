import requests as rq
from http import HTTPStatus

from .chat_model import AbstractChatModel

class ChatbaseModel(AbstractChatModel):
    def __init__(self, url: str, api_key: str, chatbot_id: str):
        super(ChatbaseModel, self).__init__()
        self.url = url
        self.api_key = api_key
        self.chatbot_id = chatbot_id
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'charset': 'utf-8'
        }

    def prepare_query(self, prompt: str):
        data_input = {
            "messages": [{'role': 'system', 
                          'content': self.get_system_message()}] + 
                          [{'role': 'user', 
                            'content': f'{prompt}'}],
            "chatbotId": self.chatbot_id,
            "stream": False,
            "temperature": 0
        }
        self.data_input = data_input

    def handle_response(self):        
        try:
            data = self.response.json()
            if self.response.status_code != HTTPStatus.OK:
                return False, f"Error:{self.response.status_code} ({data['done_reason']})"
            bot_answer = data['text']
            return True, bot_answer
        except rq.exceptions.JSONDecodeError as e:
            print(f"JSON decode error. Error:{self.response.status_code}")
            print('Input data:')
            print(self.data_input)
            print(self.response.text)
            return False, f"JSON decode error. Error:{self.response.status_code}"