from typing import List
from os import path
from glob import glob


from models import DatasetMeta

def list_dataset_groups(dataset: DatasetMeta) -> List[str]:
    """
    List all groups in a dataset.
    """
    groups = set()

    images = list_dataset_images(dataset)
    for image in images:
        group = path.dirname(image).removeprefix(dataset.path).removeprefix(path.sep)
        groups.add(group)

    print("Groups:", groups)
    return list(groups)


def list_dataset_images(dataset: DatasetMeta, groups: List[str] | None = None) -> List[str]:
    """
    List images in a dataset, either for all groups or for the specified groups.
    """

    images = []
    for format in dataset.image_formats:
        images.extend(glob(path.join(dataset.path, "**", f"*.{format}"), recursive=True))

    print("Images:", images)
    return images
