from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
  from dataclasses import dataclass
else:
  from pydantic.dataclasses import dataclass


from dataclasses import field


@dataclass
class BoundingBox:
    # 2D bounds
    top: float
    left: float
    width: float
    height: float

    # 3D bounds
    front: float = 0
    depth: float = 0

    # video bounds
    start: float = 0
    end: float = 0


@dataclass
class AnnotationMeta:
    label: str
    value: str
    bounding_box: BoundingBox | None = None


@dataclass
class ImageMeta:
    annotations: List[AnnotationMeta] = field(default_factory=list)


@dataclass
class GroupMeta:
    caption: str
    prompt: Dict[str, str] = field(default_factory=dict)
    required_labels: List[str] = field(default_factory=list)


@dataclass
class GroupMetaFile:
    group: GroupMeta
    images: Dict[str, ImageMeta] = field(default_factory=dict)


@dataclass
class DatasetMeta:
   # name: str
   path: str
   image_formats: List[str] = field(default_factory=list)


@dataclass
class AppState:
    dataset: DatasetMeta
    groups: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)

    # state stuff
    # TODO: should this really go here?
    active_group: str | None = None
    active_image: str | None = None
