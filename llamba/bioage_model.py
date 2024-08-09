import pandas as pd
import torch
from torch import nn

class BioAgeModel:
    def __init__(self, model: nn.Module):
        self.model = model

    def inference(self, data: pd.DataFrame, device: torch.device):
        self.model.to(device)
        self.model.eval()
        if str(device) == "cuda":
            res = self.model(torch.from_numpy(data.values)).cuda().detach().numpy().ravel()
        else:
            res = self.model(torch.from_numpy(data.values)).cpu().detach().numpy().ravel()
        return res
