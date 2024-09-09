from typing import List, Dict
from os import path
from glob import glob


from ..models import DatasetMeta, AppState

def count_dataset_groups(results: AppState) -> Dict[str, int]:
    """
    Count the number of images in each group in a dataset.
    """
    group_counts = {}
    for group in results.groups:
        group_counts[group] = 0

    for image in results.images:
        group = get_image_group(image, results.dataset)
        group_counts[group] += 1

    print("Group counts:", group_counts)
    return group_counts


def get_image_group(image: str, dataset: DatasetMeta) -> str:
    """
    Get the group of an image in a dataset.
    """
    group = path.dirname(image).removeprefix(dataset.path).removeprefix(path.sep)
    return group


def list_dataset_groups(dataset: DatasetMeta) -> AppState:
    """
    List all groups in a dataset.
    """
    groups = set()

    images = list_dataset_images(dataset)
    for image in images:
        group = get_image_group(image, dataset)
        groups.add(group)

    groups = list(groups)
    groups.sort()
    print("Groups:", groups)
    return AppState(dataset=dataset, groups=groups, images=images)


def list_dataset_images(dataset: DatasetMeta, groups: List[str] | None = None) -> List[str]:
    """
    List images in a dataset, either for all groups or for the specified groups.
    """

    images = []
    for format in dataset.image_formats:
        images.extend(glob(path.join(dataset.path, "**", f"*.{format}"), recursive=True))

    # TODO: filter by groups

    images.sort()
    print("Images:", images)
    return images


def list_group_images(dataset: AppState, group: str) -> List[str]:
    """
    List images in a group in a dataset.
    """
    images = []
    for image in dataset.images:
        if get_image_group(image, dataset.dataset) == group:
            images.append(image)

    images.sort()
    print("Group images:", images)
    return images
