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


def view_group(group: str, state: AppState) -> AppState:
    print("Viewing group...", group)
    new_state = AppState(**state.__dict__)
    new_state.active_group = group
    return new_state


def make_dataset_tab(dataset_state: gr.State):
    with gr.Blocks() as tab_dataset:
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
        def render_groups(state: AppState | None):
            if state is None:
                # placeholder when no dataset has been loaded
                with gr.Row(variant="panel"):
                    gr.Textbox(label="Group Name", value="group size")
                    gr.Button("View Group", interactive=False)
                return

            # count items and display links to each group
            group_counts = count_dataset_groups(state)
            for group, count in group_counts.items():
                # create a closure to capture the group name
                target_group = group

                def view_click(state, group=target_group):
                    return view_group(group, state)

                with gr.Row(variant="panel"):
                    info = f"{count} images"
                    gr.Markdown(f"### {group}\n\n{info}")
                    view = gr.Button("View Group")
                    view.click(fn=view_click, inputs=[dataset_state], outputs=[dataset_state])

        return tab_dataset
