import torch
import numpy as np
import pandas as pd
from PIL import Image
from torch import nn
from torchvision import transforms

from entities import Vehicle, Region
from services.BaseService import BaseService, Frame


class _ModelMake:
    def __init__(self, model: str, make: str):
        self.model = model
        self.make = make


class VmmrPredictorService(BaseService[_ModelMake]):
    def __init__(self, predictor_model: nn.Module, vmmr_classes: pd.DataFrame):
        self._model = predictor_model
        self._vmmr_classes = vmmr_classes
        self._device = torch.device('cuda')

    def _update_vehicle(self, vehicle: Vehicle, feature: _ModelMake):
        vehicle.model = feature.model
        vehicle.make = feature.make

    def _extract_feature(self, region: Region, preprocessed_frame: Frame) -> _ModelMake | None:
        with torch.no_grad():
            output = self._model(preprocessed_frame)
        _, preds = torch.topk(output, 3)

        preds = torch.transpose(preds, 0, 1)
        preds = preds.cpu()  # Send tensor to cpu
        preds = pd.DataFrame(preds.numpy(), columns=["Classencoded"])  # Convert to dataframe

        class_encoded_matches = pd.merge(self._vmmr_classes, preds, how="inner")
        class_encoded_matches = pd.merge(preds, class_encoded_matches, how="left", on="Classencoded", sort=False)
        classname_matches = class_encoded_matches["Classname"].unique()
        class_parts = str(classname_matches[0]).split(" ")
        make = class_parts[0]
        model = " ".join(class_parts[1:-1])
        return _ModelMake(model, make)

    def _should_process_vehicle(self, vehicle: Vehicle) -> bool:
        return vehicle.model is None and vehicle.model is None

    def _preprocess_frame(self, frame: Frame) -> np.ndarray:
        img_transforms = transforms.Compose([transforms.Resize((256, 256)),
                                             transforms.ToTensor(),
                                             transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        img = Image.fromarray(frame.astype('uint8'), 'RGB')
        img = img_transforms(img)
        img = img.to(self._device)
        img = img.unsqueeze(0)
        return img
