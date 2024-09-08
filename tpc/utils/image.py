from typing import Dict

from models import ImageMeta

def get_annotation_dict(image_meta: ImageMeta) -> Dict[str, str]:
    return {annotation.label: annotation.value for annotation in image_meta.annotations}
