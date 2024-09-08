from typing import Dict
from os import path
from yaml import load, Loader

from models import GroupMetaFile, DatasetMeta, GroupMeta

def count_group_labels(group: GroupMetaFile) -> Dict[str, int]:
    labels = {
        label: 0 for label in group.group.required_labels
    }

    for image in group.images:
        for annotation in image.annotations:
            prev = labels.get(annotation.label, 0)
            labels[annotation.label] = prev + 1

    return labels

def load_group_meta(dataset: DatasetMeta, group: str) -> GroupMetaFile:
    meta_path = path.join(dataset.path, group, "meta.yaml")
    if not path.exists(meta_path):
        return GroupMetaFile(group=GroupMeta(caption=""), images={})

    with open(meta_path, "r") as file:
        meta = load(file, Loader=Loader)

    return GroupMetaFile(**meta)
