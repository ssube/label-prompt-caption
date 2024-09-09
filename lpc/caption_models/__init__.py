from .joy import caption_with_joy
from .florence import caption_with_florence
from .moondream import caption_with_moondream
from .wd import caption_with_wd, caption_with_dd, caption_with_mld

CAPTION_CALLBACKS = {
    "Florence": caption_with_florence,
    "Joy": caption_with_joy,
    "Moondream": caption_with_moondream,
    # older tag models
    "DeepDanbooru": caption_with_dd,
    "MLDanbooru": caption_with_mld,
    "WaifuDiffusion": caption_with_wd,
}
