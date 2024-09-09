from typing import List, Tuple

import gradio as gr

from args import IMAGE_FORMATS
from models import DatasetMeta, AppState, GroupMetaFile
from utils.dataset import list_dataset_groups, count_dataset_groups
from utils.group import load_group_meta


def load_dataset(name: str, path: str, image_formats: List[str]):
    print("Loading dataset...", name, path, image_formats)
    dataset = DatasetMeta(name=name, path=path, image_formats=image_formats)
    results = list_dataset_groups(dataset)
    print("Results:", results)
    return results


def view_group(group: str, state: AppState) -> Tuple[AppState, GroupMetaFile]:
    print("Viewing group...", group)
    new_state = AppState(**state.__dict__)
    new_state.active_group = group

    group_state = load_group_meta(new_state.dataset, group)
    return new_state, group_state


def make_dataset_tab(dataset_state: gr.State, group_state: gr.State):
    with gr.Blocks() as tab_dataset:
        with gr.Row():
            dataset_name = gr.Textbox(label="Dataset Name", placeholder="my_dataset")

        with gr.Row():
            dataset_path = gr.Textbox(label="Base Path", placeholder="path/to/images")
            dataset_formats = gr.CheckboxGroup(choices=IMAGE_FORMATS, label="Image Formats", value=IMAGE_FORMATS)

        with gr.Row():
            load = gr.Button("Load Groups")
            load.click(fn=load_dataset, inputs=[dataset_name, dataset_path, dataset_formats], outputs=[dataset_state])

        @gr.render(inputs=[dataset_state, group_state])
        def render_groups(state: AppState | None, group_meta: GroupMetaFile | None):
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
                    view.click(fn=view_click, inputs=[dataset_state], outputs=[dataset_state, group_state])

        return tab_dataset
