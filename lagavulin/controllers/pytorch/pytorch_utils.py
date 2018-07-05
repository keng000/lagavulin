import torch
def load_pytorch_model(model, serialized_model_path):
    try:
        model.load_state_dict(torch.load(serialized_model_path))
    except AssertionError:
        model.load_state_dict(torch.load(serialized_model_path, map_location=lambda storage, loc: storage))

    return model

