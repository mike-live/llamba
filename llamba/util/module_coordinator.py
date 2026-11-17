from llamba.util.module import Module
from llamba.chatmodels.chat_model import BaseChatModel
from llamba.util.strings.language_manager import get_string
import pandas as pd

class ModuleCoordinator:
    def __init__(self):
        self.modules: dict[str, Module] = {}
        self.device = ""
        self.analyze_feats = False
        self.analyze_risks = False

    def add_module(self, module: Module, 
                   chat_model: BaseChatModel,
                   **kwargs):
        for key, value in kwargs.items():
            setattr(module, key, value)
        module.chat_model = chat_model
        self.modules[module.name] = module

    def get_module(self, tag):
        return self.modules[tag]

    def analyze(self, data: pd.DataFrame, **kwargs) -> str:
        full_analysis = ""
        for module_name, module in self.modules.items():
            for key, value in kwargs.items():
                setattr(module, key, value)
            module_data = data[module.feats]
            analysis = module.analyze(module_data, **kwargs)
            full_analysis += analysis['analysis']
            if module_name == 'bioage':
                full_analysis += get_string("additional_analysis")
        return full_analysis