class AbstractChatModel:
    def __init__(self): pass
    def get_system_message(self):
        return 'I want you to act a gerontology expert. Answer prompts shortly, without emotions and greetings, and in the same language they are asked.'

    def prepare_query(self, prompt):
        data_input = {
            "messages": self.get_system_message() + [{'role': 'user', 'content': f'{prompt}'}]
        }
        self.data_input = data_input

    def query(self, prompt):
        self.prepare_query(prompt)
        return f'You have a very nice prompt: {self.data_input}.'