import pandas as pd
import torch
from torch import nn

class BioAgeModel:
    def __init__(self, model: nn.Module):
        self.model = model

    def inference(self, data: pd.DataFrame):
        self.model.eval()
        try:
            res = self.model(torch.from_numpy(data.values)).cpu().detach().numpy().ravel()
        except:
            res = 55
        return res
