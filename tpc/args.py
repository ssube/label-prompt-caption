import torch

MODEL_DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
MODEL_FORMAT = torch.float16 if torch.cuda.is_available() else torch.float32

CAPTION_MODELS = ["Joy", "Florence"] # , "DeepDanbooru", "MLDanbooru", "WaifuDiffusion"]
IMAGE_FORMATS = ["jpg", "jpeg", "png"]

DATASET_FILE = "dataset.yaml"
GROUP_FILE = "meta.yaml"
