from typing import Iterable

import matplotlib.pyplot as plt
from matplotlib import patches, patheffects


def show_image(img, ax=None, figsize=None, alpha=1.0):
    if ax is None: fig, ax = plt.subplots(figsize=figsize)

    ax.imshow(img, alpha=alpha)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    return ax


def draw_outline(obj, lw=4):
    obj.set_path_effects([patheffects.Stroke(linewidth=lw, foreground='black'), patheffects.Normal()])


def draw_bbox(ax, bbox, color='white'):
    patch = ax.add_patch(patches.Rectangle(bbox[:2], *bbox[-2:], fill=False, edgecolor=color, lw=2))
    draw_outline(patch)


def draw_text(ax, xy, text, size=14, color='white'):
    text = ax.text(*xy, text, verticalalignment='top', color=color, fontsize=size, weight='bold')
    draw_outline(text)


def Intersection_over_Union(object_box_coords, true_box_coords):
    """
    IoU値を計算する。
    :param object_box_coords: tuple/list. (left, top, right, bottom)
    :param true_box_coords: tuple/list. (left, top, right, bottom)
    :return: IoU value
    """
    for element in [object_box_coords, true_box_coords]:
        assert isinstance(element, list) or isinstance(element, tuple), TypeError
        assert len(element) == 4, ValueError

    # 2領域が被覆していない場合、被覆領域の値を0に.
    if (true_box_coords[0] > object_box_coords[2] or true_box_coords[2] < object_box_coords[0]
            or true_box_coords[1] > object_box_coords[3] or true_box_coords[3] < object_box_coords[1]):
        interArea = 0

    else:
        xA = max(object_box_coords[0], true_box_coords[0])
        yA = max(object_box_coords[1], true_box_coords[1])
        xB = min(object_box_coords[2], true_box_coords[2])
        yB = min(object_box_coords[3], true_box_coords[3])

        interArea = (xB - xA + 1) * (yB - yA + 1)

    boxAArea = (object_box_coords[2] - object_box_coords[0] + 1) * (object_box_coords[3] - object_box_coords[1] + 1)
    boxBArea = (true_box_coords[2] - true_box_coords[0] + 1) * (true_box_coords[3] - true_box_coords[1] + 1)

    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou


def visualize_segment_map(
        base_img: np.ndarray, segment_map: np.ndarray, class_num: int,
        ignore_class: Iterable[int], plot: bool =True, is_gray_scale: bool =False
):
    """
    Visualize function for Semantic Segmentation.
    :param base_img:
    :param segment_map: same size with base_img. when the class variation is 0~4,
                            then each element in segment_map would be 0~4.
    :param class_num: the number of class. this function assume the label is continuous within 0~class_num.
    :param ignore_class:
    :param plot: if true, then the base_img and segment_map would be plotted.
    :param is_gray_scale: if true, then the image would converted before plotting.
    :return:
    """
    Sky = [128, 128, 128]
    Building = [128, 0, 0]
    Pole = [192, 192, 128]
    Road_marking = [255, 69, 0]
    Road = [128, 64, 128]
    Pavement = [60, 40, 222]
    Tree = [128, 128, 0]
    SignSymbol = [192, 128, 128]
    Fence = [64, 64, 128]
    Car = [64, 0, 128]
    Pedestrian = [64, 64, 0]
    Bicyclist = [0, 128, 192]
    Unlabelled = [0, 0, 0]

    label_colours = np.array([Unlabelled, Sky, Building, Pole, Road_marking, Road, Pavement,
                              Tree, SignSymbol, Fence, Car, Pedestrian, Bicyclist])

    r = segment_map.copy()
    g = segment_map.copy()
    b = segment_map.copy()
    for l in range(0, class_num):
        if l in ignore_class:
            continue
        r[segment_map == l] = label_colours[l, 0]
        g[segment_map == l] = label_colours[l, 1]
        b[segment_map == l] = label_colours[l, 2]

    rgb = np.zeros((segment_map.shape[0], segment_map.shape[1], 3))
    rgb[:, :, 0] = (r / 255.0)
    rgb[:, :, 1] = (g / 255.0)
    rgb[:, :, 2] = (b / 255.0)

    if plot:
        if is_gray_scale:
            base_img = cv2.cvtColor(base_img, cv2.COLOR_GRAY2RGB)
        ax = show_image(base_img)
        show_image(segment_map, ax=ax, alpha=0.6)
        plt.show()
    else:
        return rgb
