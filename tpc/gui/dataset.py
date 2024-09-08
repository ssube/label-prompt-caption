from typing import List

import gradio as gr

from models import DatasetMeta
from utils.dataset import list_dataset_groups, count_dataset_groups


def load_dataset(name: str, path: str, image_formats: List[str]):
    print("Loading dataset...", name, path, image_formats)
    dataset = DatasetMeta(name=name, path=path, image_formats=image_formats)
    results = list_dataset_groups(dataset)
    print("Results:", results)
    return results


with gr.Blocks() as tab_dataset:
    dataset_state = gr.State()

    gr.Markdown("### Dataset")
    with gr.Row():
        dataset_name = gr.Textbox(label="Dataset Name", placeholder="my_dataset")

    with gr.Row():
        dataset_path = gr.Textbox(label="Base Path", placeholder="path/to/images")
        dataset_formats = gr.CheckboxGroup(["jpg", "jpeg", "png"], label="Image Formats")

    with gr.Row():
        load = gr.Button("Load Groups")
        load.click(fn=load_dataset, inputs=[dataset_name, dataset_path, dataset_formats], outputs=[dataset_state])

    with gr.Row() as group_row:
        @gr.render(inputs=[dataset_state])
        def render_groups(results):
            if results is None:
                return gr.Textbox(label="Group Name", value="group size")

            group_counts = count_dataset_groups(results)

            return [gr.Textbox(label=group, value=str(count)) for group, count in group_counts.items()]

