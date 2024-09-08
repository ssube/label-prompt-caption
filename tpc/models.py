from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
  from dataclasses import dataclass
else:
  from pydantic.dataclasses import dataclass


@dataclass
class BoundingBox:
    top: int
    left: int
    width: int
    height: int


@dataclass
class AnnotationMeta:
    label: str
    value: str
    bounding_box: BoundingBox | None = None


@dataclass
class ImageMeta:
    annotations: List[AnnotationMeta]


@dataclass
class GroupMeta:
    caption: str
    prompt: str = ''


@dataclass
class GroupMetaFile:
    group: GroupMeta
    images: Dict[str, ImageMeta]


@dataclass
class DatasetMeta:
   image_formats: List[str]
   name: str
   path: str


@dataclass
class AppState:
    dataset: DatasetMeta
    groups: List[str]
    images: List[str]

    # state stuff
    # TODO: should this really go here?
    active_group: str | None = None
    active_image: str | None = None
