from llamba.chatmodels.chat_model import BaseChatModel
from llamba.util.strings.language_manager import get_string
from llamba.util.clock import Clock
import pandas as pd

class Module:
    def __init__(self, feats: list[str]):
        self.name = ""
        self.chat_model = BaseChatModel()
        self.document_repo = None
        self.clock: Clock = ""
        self.condition = ""
        self.answer = ""
        self.feats = feats
        self.language = "ru"

    # Prompt querying
    def query_prompt(self, prompt: str):
        if self.document_repo:
            try:
                context = self.document_repo.search(prompt)
                prompt += get_string("context", context=context)
            except:
                pass
        if self.clock:
            clock_prompt = get_string("clock", clock_name=self.clock.name, clock_doi=self.clock.doi)
            prompt = clock_prompt + prompt
        res = self.chat_model.query(prompt=prompt)[1]
        return res

    def query_prompts(self, prompts: list):
        answer = ""
        for prompt in prompts:
            res = self.query_prompt(prompt)
            answer += res
            answer += '\n\n'
        return answer

    def analyze(self, data: pd.DataFrame):
        pass