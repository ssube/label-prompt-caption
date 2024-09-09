from typing import Dict
from os import path
from yaml import load, Loader, dump

from ..args import GROUP_FILE
from ..models import GroupMetaFile, DatasetMeta, GroupMeta

def count_group_labels(group: GroupMetaFile) -> Dict[str, int]:
    labels = {
        label: 0 for label in group.group.required_labels
    }

    for image_name, image_meta in group.images.items():
        for annotation in image_meta.annotations:
            prev = labels.get(annotation.label, 0)
            labels[annotation.label] = prev + 1

    return labels

def load_group_meta(dataset: DatasetMeta, group: str) -> GroupMetaFile:
    meta_path = path.join(dataset.path, group, GROUP_FILE)
    if not path.exists(meta_path):
        print("Creating new group metadata:", group)
        return GroupMetaFile(group=GroupMeta(caption=""), images={})

    print("Loading group metadata:", group)
    with open(meta_path, "r") as file:
        return load(file, Loader=Loader)

def save_group_meta(dataset: DatasetMeta, group: str, group_meta: GroupMetaFile) -> None:
    meta_path = path.join(dataset.path, group, GROUP_FILE)
    print("Saving group metadata:", group, meta_path)
    with open(meta_path, "w") as file:
        dump(group_meta, file)
