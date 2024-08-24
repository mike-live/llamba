from llamba.chat_model import AbstractChatModel
from llamba.bioage_model import BioAgeModel
from llamba.connector import LlambaConnector
import torch
from torch import nn
import pandas as pd
import numpy as np

# Test for local machine only, since API keys can't be transferred to github safely
# Possible workaround -- self-hosted test runner
def test_query():
    # Prepare data to analyze
    num_features = 10
    features = np.random.randint(low=1, high=150, size=num_features).astype(np.float32)
    age =  np.random.randint(low=10, high=90)

    data = pd.DataFrame([{f'Feature_{i}' : features[i] for i in range(num_features)}])
    data['Age'] = age

    # Prepare a BioAge model
    class DummyBioAgeModel(nn.Module): 
        def __init__(self): 
            super(DummyBioAgeModel, self).__init__()
            self.linear1 = torch.nn.Linear(10, 1)

        def forward(self, x):
            x = self.linear1(x)
            return abs(x)

    model = DummyBioAgeModel()
    bioage_model = BioAgeModel(model)

    # Prepare a Chatbot model
    class DummyChatModel(AbstractChatModel): pass
    chat_model = DummyChatModel()
    connector = LlambaConnector(bioage_model=bioage_model, chat_model=chat_model)

    res = connector.analyze(data)
    print(res['analysis'])