from typing import List

import gradio as gr

from models import DatasetMeta
from utils.dataset import list_dataset_groups


def load_dataset(name: str, path: str, image_formats: List[str]):
    print("Loading dataset...", name, path, image_formats)
    dataset = DatasetMeta(name=name, path=path, image_formats=image_formats)
    groups = list_dataset_groups(dataset)
    print("Groups:", groups)
    return groups


with gr.Blocks() as tab_dataset:
    gr.Markdown("### Dataset")
    with gr.Row():
        dataset_name = gr.Textbox(label="Dataset Name", placeholder="my_dataset")

    with gr.Row():
        dataset_path = gr.Textbox(label="Base Path", placeholder="path/to/images")
        dataset_formats = gr.CheckboxGroup(["jpg", "jpeg", "png"], label="Image Formats")

    with gr.Row():
        load = gr.Button("Load Groups")

    with gr.Row():
        dataset_groups = gr.TextArea(label="Found Groups", placeholder="group1, group2, ...")

    load.click(fn=load_dataset, inputs=[dataset_name, dataset_path, dataset_formats], outputs=[dataset_groups])
