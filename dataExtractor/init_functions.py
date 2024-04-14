import torch
import pandas as pd
from torchvision import models


def init_vmmr_predictor(vmmr_model_path: str, vmmr_classes_path_pkl: str) -> (pd.DataFrame, torch.nn.Module):
    vmmr_classes = pd.read_pickle(vmmr_classes_path_pkl)

    weights = models.ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)
    device = torch.device('cuda')
    fc_in_feats = model.fc.in_features
    model.fc = torch.nn.Linear(fc_in_feats, vmmr_classes["Classname"].nunique())
    model.load_state_dict(torch.load(vmmr_model_path, map_location=device))
    model.to(device)
    model.eval()
    return vmmr_classes, model
