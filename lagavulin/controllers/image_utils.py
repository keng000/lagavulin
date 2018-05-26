import matplotlib.pyplot as plt
from matplotlib import patches, patheffects


def show_image(img, ax=None, figsize=None):
    if ax is None: fig, ax = plt.subplots(figsize=figsize)

    ax.imshow(img)
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

