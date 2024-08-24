import json
import requests as rq

from llamba.chat_model import AbstractChatModel

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