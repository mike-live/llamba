from llamba.util.module import Module
from llamba.util.strings.language_manager import get_string
import pandas as pd
import numpy as np

class MortalityPredictor(Module):
    def __init__(self, model, disease_name, **kwargs):
        super().__init__(**kwargs)
        self.name = disease_name
        self.mortality_predictor = model

    # Accepts data as a pandas DataFrame, containing necessary features and their values
    def analyze(self, data: pd.DataFrame, **kwargs):
        mortality = self.mortality_predictor.predict_mortality(data)
        self.answer += get_string("mortality_opening", name=self.name)
        if np.isclose(mortality, 1.0):
            self.answer += get_string("mortality_1")
        else:
            self.answer += get_string("mortality_0")
        return {'analysis': self.answer}
