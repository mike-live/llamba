from llamba_framework.chatmodels.chat_model import AbstractChatModel
from llamba.bioage_model import BioAgeModel
from llamba.connector import LlambaConnector
import torch
from torch import nn
import pandas as pd
import numpy as np
import unittest

class TestAnalyzeFunction(unittest.TestCase):
    def test_query(self):
        # Prepare data to analyze
        np.random.seed(0)
        torch.manual_seed(0)
        num_features = 10
        features = np.random.randint(low=1, high=150, size=num_features).astype(np.float32)
        age =  np.random.randint(low=10, high=90)

        data = pd.DataFrame([{f'Feature_{i}' : features[i] for i in range(num_features)}])
        data['Age'] = age

        print(data)

        # Prepare a BioAge model
        class DummyBioAgeModel(nn.Module): 
            def __init__(self): 
                super(DummyBioAgeModel, self).__init__()
                self.linear = torch.nn.Linear(10, 1)

            def forward(self, x):
                x = self.linear(x)
                return abs(x)

        model = DummyBioAgeModel()
        bioage_model = BioAgeModel(model)

        # Prepare a Chatbot model
        class DummyChatModel(AbstractChatModel): pass
        chat_model = DummyChatModel()
        connector = LlambaConnector(bioage_model=bioage_model, chat_model=chat_model)

        res = connector.analyze(data)
        print(res['analysis'])
        self.assertEqual(str.strip(res['analysis']), "Your bioage is 6 and your aging acceleration is -16, which means you are ageing slower than normal.")

if __name__ == '__main__':
    unittest.main()