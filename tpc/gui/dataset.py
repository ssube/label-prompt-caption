from typing import List

import gradio as gr

from models import DatasetMeta, AppState
from utils.dataset import list_dataset_groups, count_dataset_groups


def load_dataset(name: str, path: str, image_formats: List[str]):
    print("Loading dataset...", name, path, image_formats)
    dataset = DatasetMeta(name=name, path=path, image_formats=image_formats)
    results = list_dataset_groups(dataset)
    print("Results:", results)
    return results


def view_group(group: str, results: AppState) -> AppState:
    print("Viewing group...", group)
    results.active_group = group
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

    @gr.render(inputs=[dataset_state])
    def render_groups(results):
        if results is None:
            # placeholder when no dataset has been loaded
            with gr.Row(variant="panel"):
                gr.Textbox(label="Group Name", value="group size")
                gr.Button("View Group", interactive=False)
            return

        # count items and display links to each group
        group_counts = count_dataset_groups(results)
        for group, count in group_counts.items():
            with gr.Row(variant="panel"):
                info = f"{count} images"
                gr.Markdown(f"### {group}\n\n{info}")
                view = gr.Button("View Group")
                view.click(fn=lambda state: view_group(group, state), inputs=[dataset_state], outputs=[dataset_state])
