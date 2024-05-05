class ChatModel:
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key

class Task:
    def __init__(self):
        ...

class Connector:
    def __init__(self, bioage_model: object, chat_model: ChatModel):
        self.bioage_model = bioage_model
        self.chat_model = chat_model

    def analyze(self, data):
        

    
    
