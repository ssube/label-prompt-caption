from .clip import caption_with_clip
from .florence import caption_with_florence
from .joy import caption_with_joy

CAPTION_CALLBACKS = {
    "CLIP": caption_with_clip,
    "Florence": caption_with_florence,
    "Joy": caption_with_joy,
}
