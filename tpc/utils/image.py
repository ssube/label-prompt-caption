from os import path
from typing import Dict

from models import ImageMeta

def get_annotation_dict(image_meta: ImageMeta) -> Dict[str, str]:
    return {annotation.label: annotation.value for annotation in image_meta.annotations}


def load_image_caption(image: str) -> str:
    caption_file = path.splitext(image)[0] + ".txt"

    try:
        with open(caption_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def save_image_caption(image: str, caption: str) -> None:
    caption_file = path.splitext(image)[0] + ".txt"
    print(f"Saving caption to {caption_file}: {caption}")

    with open(caption_file, "w") as f:
        f.write(caption)

