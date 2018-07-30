import torch
from pathlib import Path
from typing import Union


class PytorchModelLoader:
    def __init__(self, model: torch.nn.Module):
        self.model = model

    def get_model(self, trained_model_path=None) -> torch.nn.Module:
        if trained_model_path:
            self.model = self._load_serialized_model(self.model, trained_model_path)

        if torch.cuda.is_available():
            return self.model.cuda()

        return self.model

    def _load_serialized_model(self, model: torch.nn.Module, serialized_model_path: Union[str, Path]):
        try:
            model.load_state_dict(torch.load(serialized_model_path))
        except AttributeError:
            model.load_state_dict(torch.load(serialized_model_path, map_location=lambda storage, loc: storage))

        return model
