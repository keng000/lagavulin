from typing import Iterable
import matplotlib.pyplot as plt
from matplotlib import patches, patheffects
import numpy as np


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __getitem__(self, idx):
        if idx == 0: return self.x
        if idx == 1: return self.y
        raise IndexError


class BBox:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self.__min = Point(left, top)
        self.__max = Point(right, bottom)
        self.height = self._height()
        self.width = self._width()

    def get_min_point(self) -> Point:
        return self.__min
    
    def get_max_point(self) -> Point:
        return self.__max
    
    def _width(self) -> int:
        return self.__max.x - self.__min.x
    
    def _height(self) -> int:
        return self.__max.y - self.__min.y

    def is_covered(self, bbox):
        assert isinstance(bbox, BBox)
        if self.__min.x > bbox.__max.x: return False
        if self.__max.x < bbox.__min.x: return False
        if self.__min.y > bbox.__max.y: return False
        if self.__max.y < bbox.__min.y: return False
        return True
    
    def intersection_over_union(self, bbox):
        assert isinstance(bbox, BBox)

        # 2領域が被覆していない場合、被覆領域の値を0に.
        if self.is_covered(bbox):
            interArea = 0

        else:
            xA = max(self.__min.x, bbox.__min.x)
            yA = max(self.__min.y, bbox.__min.y)
            xB = min(self.__max.x, bbox.__max.x)
            yB = min(self.__max.y, bbox.__max.y)

            interArea = (xB - xA + 1) * (yB - yA + 1)

        boxAArea = (bbox.height + 1) * (bbox.width + 1)
        boxBArea = (self.height + 1) * (self.width + 1)

        iou = interArea / float(boxAArea + boxBArea - interArea)
        return iou


def show_image(image, ax=None, figsize=None, size_factor=16, alpha=1.0, show=True):
    if figsize is None:
        height = int(image.shape[0] / float(max(image.shape[:2])) * size_factor)
        width = int(image.shape[1] / float(max(image.shape[:2])) * size_factor)
        figsize = (width, height)

    if ax is None: fig, ax = plt.subplots(figsize=figsize)

    ax.imshow(image, alpha=alpha)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    if show:
        plt.show()
    return ax


def draw_bbox(ax, bbox: BBox, color='white'):
    patch = ax.add_patch(patches.Rectangle(bbox.get_min_point(), bbox.width, bbox.height, fill=False, edgecolor=color, lw=2))
    draw_outline(patch)


def draw_outline(obj, lw=4):
    obj.set_path_effects([patheffects.Stroke(linewidth=lw, foreground='black'), patheffects.Normal()])


def draw_text(ax, point: Point, text, size=14, color='white'):
    text = ax.text(point.x, point.y, text, verticalalignment='top', color=color, fontsize=size, weight='bold')
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
        ignore_class: Iterable[int] = (), is_gray_scale: bool = False
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

    if is_gray_scale:
        base_img = cv2.cvtColor(base_img, cv2.COLOR_GRAY2RGB)
    ax = show_image(base_img, show=False)
    show_image(segment_map, ax=ax, alpha=0.6)
    plt.show()

