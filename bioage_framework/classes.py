import json
import requests as rq
import aiohttp

class ChatModel:
    def __init__(self, url: str, api_key: str, chatbot_id: str):
        self.url = url
        self.api_key = api_key
        self.chatbot_id = chatbot_id
        self.system_message = [{
            'role': 'system',
            'content':
                '''
                I want you to act as an expert in gerontology. Answer prompts in the same language they are asked.
                '''
        }]
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'accept': 'application/json',
            'charset': 'utf-8'
        }

    def prepare_query(self, prompt):
        data_input = {
            "messages": self.system_message + [{'role': 'user', 'content': f'{prompt}'}],
            "chatbotId": self.chatbot_id,
            "stream": False,
            "temperature": 0
        }
        self.data_input = data_input

    def query(self, prompt):
        self.prepare_query(prompt)
        data_input_json = json.dumps(self.data_input).encode('utf-8')
        
        num_tries = 2
        for _ in range(num_tries):
            response = rq.post(self.url, headers=self.headers, data=data_input_json, timeout=30)
            if response.status_code != 405:
                break

        try:
            data = response.json()
            if response.status_code != 200:
                return False, f"Error:{response.status_code}({data['message']})"
            bot_answer = data['text']
            return True, bot_answer
        except rq.exceptions.JSONDecodeError as e:
            print(f"JSON decode error. Error:{response.status_code}")
            print('Input data:')
            print(data_input_json)
            print(response.text)
            return False, f"JSON decode error. Error:{response.status_code}"

class Task:
    def __init__(self):
        ...

class Connector:
    def __init__(self, bioage_model: object, chat_model: ChatModel):
        self.bioage_model = bioage_model
        self.chat_model = chat_model

    def analyze(self, task):
        ...
