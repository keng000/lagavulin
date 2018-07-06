class asGrayScale(object):
    def __call__(self, input):
        img, segmap = input
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return np.reshape(img, img.shape + (1,)), segmap


class RandomRotate(object):
    def __init__(self, degree):
        self.degree = degree

    def __call__(self, input):
        img, mask = input
        rotate_degree = random.random() * 2 * self.degree - self.degree
        # return img.rotate(rotate_degree, Image.BILINEAR), mask.rotate(rotate_degree, Image.NEAREST)
        return ndimage.rotate(img, rotate_degree, cval=255, reshape=False), ndimage.rotate(mask, rotate_degree, mode='nearest')


class Squareization(object):
    def __call__(self, input):
        """
        入力画像を白埋めで正方形に整える。また、セグメンテーションマップも Non-Classで埋める。
        :param input: 画像と対応するセグメンテーションマップのTuple
            image: 2D(gray) / 3D(color) 行列で、各次元の意味は [H, W] または [H, W, C]。 ※ [C, H, W] を入力しない様に注意。
            segment map: 2D 行列。
        :return:
        """
        img, segmap = input
        # assert len(img.shape) == 3, ValueError(f"Dim Error. Imput dim == {img.shape} , where assumed dim == 3")

        img_height, img_width = img.shape[:2]
        if img_height == img_width:
            # 正方形レシート. この場合何も処理する必要が無い理想形ため、入力そのまま返す。
            return input

        edge_length_diff = abs(img_height - img_width)
        padding_top_left = padding_bottom_right = edge_length_diff // 2
        if edge_length_diff % 2 == 1:
            padding_bottom_right += 1

        if img_height > img_width:
            # 縦長レシート。左右に余白を加える。
            pad_width = [(0, 0), (padding_top_left, padding_bottom_right)]

        else:
            # 横長レシート。上下に余白を加える。
            pad_width = [(padding_top_left, padding_bottom_right), (0, 0)]

        reshaped_segmap = np.pad(segmap, pad_width, mode="constant", constant_values=0)

        is_color = len(img.shape) == 3
        if is_color:
            pad_width += [(0, 0)]

        reshaped_img = np.pad(img, pad_width, mode='constant', constant_values=255)
        return reshaped_img, reshaped_segmap


class Reformat(object):
    def __call__(self, input):
        img, segmap = input
        in_size = 572

        resized_img = skimage_resize(img, (in_size, in_size), mode='constant', cval=255)

        resized_map = cv2.resize(segmap, (in_size, in_size), interpolation=cv2.INTER_NEAREST)
        resized_map = resized_map.astype(np.uint8)

        # TODO: 原因不明(おそらくResize関数の補完メソッド)でクラス番号4が1,2こ出現するため、クラス0で上書きする。
        resized_map[resized_map == 4] = 0
        assert all([class_num in [0, 1, 2, 3] for class_num in np.unique(resized_map)]), \
            ValueError("Unknown class number", np.unique(resized_map))

        resized_img = np.transpose(resized_img, (2, 0, 1))

        resized_img -= 127
        resized_img /= 255.

        return resized_img, resized_map

