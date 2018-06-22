


import torch
def load_pytorch_model(model, serialized_model_path):
    try:
        model.load_state_dict(torch.load(serialized_model_path))
    except AssertionError:
        model.load_state_dict(torch.load(serialized_model_path, map_location=lambda storage, loc: storage))

    return model

def visualize_segment_map(segment_map: np.ndarray, plot=True):
    # for semantic segmentation visualization
    Sky = [128,128,128]
    Building = [128,0,0]
    Pole = [192,192,128]
    Road_marking = [255,69,0]
    Road = [128,64,128]
    Pavement = [60,40,222]
    Tree = [128,128,0]
    SignSymbol = [192,128,128]
    Fence = [64,64,128]
    Car = [64,0,128]
    Pedestrian = [64,64,0]
    Bicyclist = [0,128,192]
    Unlabelled = [0,0,0]
    
    label_colours = np.array([Sky, Building, Pole, Road, Pavement, 
        Tree, SignSymbol, Fence, Car, Pedestrian, Bicyclist, Unlabelled])
    
    r = segment_map.copy()
    g = segment_map.copy()
    b = segment_map.copy()
    for l in range(0,11):
        r[segment_map==l]=label_colours[l,0]
        g[segment_map==l]=label_colours[l,1]
        b[segment_map==l]=label_colours[l,2]

    rgb = np.zeros((segment_map.shape[0], segment_map.shape[1], 3))
    rgb[:,:,0] = (r/255.0)
    rgb[:,:,1] = (g/255.0)
    rgb[:,:,2] = (b/255.0)
    if plot:
        plt.imshow(rgb)
    else:
        return rgb
