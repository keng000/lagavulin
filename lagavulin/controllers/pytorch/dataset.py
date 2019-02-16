import shutil
from pathlib import Path
from typing import Tuple

from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.datasets.folder import find_classes, make_dataset, IMG_EXTENSIONS
from torchvision.transforms import Compose
from tqdm import tqdm


def create_imagefolder_dataloader(
        data_source_path: Path, transform: Compose = None, test_transform: Compose = None,
        batch_size=64, num_workers=4) -> Tuple[DataLoader, DataLoader]:
    """
    torchvision.datasets.ImageFolder用のデータローダー生成関数

    Args:
        data_source_path:
        transform:
        test_transform:
        batch_size:
        num_workers:

    Returns:

    """
    data_transforms = {
        'train': transform,
        'val': test_transform
    }

    image_datasets = {
        x: ImageFolder(str(data_source_path / x), data_transforms[x])
        for x in ['train', 'val']
    }

    dataloaders = {
        x: DataLoader(image_datasets[x],
                      batch_size=batch_size,
                      shuffle=True,
                      num_workers=num_workers)
        for x in ['train', 'val']
    }

    return dataloaders["train"], dataloaders["val"]


def train_test_split_for_dir(root_path: Path, test_size: float, random_state: int = 42):
    """
    torchvision.datasets.ImageFolder 形式のディレクトリ構造になっているデータセットを train / test に分割し、
    train, testそれぞれを `root_path` と同じ階層に `train/` `val/` して保存する。

    TODO: この関数内でTrain, Test用のImageFolderを作成する方が良いのか考える。
    """
    if not root_path.exists():
        raise FileNotFoundError
    elif not (0 <= test_size <= 1.0):
        raise ValueError

    classes, class_to_idx = find_classes(root_path)
    dataset = make_dataset(root_path, class_to_idx, IMG_EXTENSIONS)
    train, val = train_test_split(dataset, test_size=test_size, shuffle=True, random_state=random_state)

    split_dataset = {'train': train, 'val': val}

    dst_path_root = root_path.parent
    for set_ in ['train', 'val']:
        for file_path, class_ in tqdm(split_dataset[set_], desc=set_):
            file_path = Path(file_path)
            dst_dir = dst_path_root / set_ / str(class_)
            dst_dir.mkdir(exist_ok=True, parents=True)
            shutil.copy(file_path, dst_dir / file_path.name)

