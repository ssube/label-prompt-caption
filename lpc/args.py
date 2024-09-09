import torch
from argparse import ArgumentParser
from typing import NamedTuple

MODEL_DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
MODEL_FORMAT = torch.float16 if torch.cuda.is_available() else torch.float32

CAPTION_MODELS = ["Joy", "Florence", "Moondream"] # , "DeepDanbooru", "MLDanbooru", "WaifuDiffusion"]
IMAGE_FORMATS = ["jpg", "jpeg", "png"]

# DATASET_FILE = "dataset.yaml"
GROUP_FILE = "meta.yaml"

class Args(NamedTuple):
    caption_models: list[str]
    image_formats: list[str]
    model_device: str
    model_format: torch.dtype
    dataset_file: str
    group_file: str

def parse_args() -> Args:
    parser = ArgumentParser()

    # list args
    parser.add_argument("--caption-models", type=str, nargs="+", default=CAPTION_MODELS)
    parser.add_argument("--image-formats", type=str, nargs="+", default=IMAGE_FORMATS)

    # device args
    parser.add_argument("--model-device", type=str, default=MODEL_DEVICE)
    parser.add_argument("--model-format", type=str, default=MODEL_FORMAT)

    # file args
    # parser.add_argument("--dataset-file", type=str, default=DATASET_FILE)
    parser.add_argument("--group-file", type=str, default=GROUP_FILE)

    return parser.parse_args()
