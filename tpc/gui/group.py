import gradio as gr
# from os import path

from args import CAPTION_MODELS
from models import AppState, GroupMetaFile
from utils.dataset import list_group_images
from utils.group import count_group_labels, load_group_meta

def view_image(image: str, state: AppState) -> AppState:
    print("Viewing image...", image)
    new_state = AppState(**state.__dict__)
    new_state.active_image = image
    return new_state


def add_group_label(group_state: GroupMetaFile, label: str) -> GroupMetaFile:
    print("Adding label...", label)
    new_group_state = GroupMetaFile(**group_state.__dict__)
    new_group_state.group.required_labels.append(label)
    return new_group_state


def load_group_state(dataset_state: AppState) -> GroupMetaFile:
    print("Loading group state...", dataset_state.active_group)
    group_meta = load_group_meta(dataset_state.dataset, dataset_state.active_group)
    return group_meta


def save_group_state(dataset_state: AppState, group_state: GroupMetaFile) -> None:
    print("Saving group state...", dataset_state.active_group, group_state)


def make_group_tab(dataset_state: gr.State):
    with gr.Blocks() as tab_group:
        group_state = gr.State()

        @gr.render(inputs=[dataset_state, group_state])
        def render_group(state: AppState, group_meta: GroupMetaFile):
            active_group = state.active_group or "none"
            print("Rendering group...", active_group)

            if state is None or state.active_group is None:
                with gr.Row():
                    gr.Textbox(label="Group Name", value="none")
                    return

            with gr.Row():
                gr.Textbox(label="Group Name", value=active_group)

            with gr.Row():
                load = gr.Button("Load Group Meta")
                load.click(fn=load_group_state, inputs=[dataset_state], outputs=[group_state])
                save = gr.Button("Save Group Meta")
                save.click(fn=save_group_state, inputs=[dataset_state, group_state])

            if group_meta:
                with gr.Row():
                    gr.Textbox(label="Group Caption", placeholder="Group caption")

                with gr.Accordion("Group Prompts"):
                    for model in CAPTION_MODELS:
                        gr.Textbox(label=model, placeholder=f"{model} prompt", value=group_meta.group.prompt.get(model, ""))

                with gr.Accordion("Group Taxonomy"):
                    with gr.Row():
                        group_labels = count_group_labels(group_meta)
                        gr.Dataframe(
                            headers=["Label", "Count"],
                            value=[[label, count] for label, count in group_labels.items()],
                        )

                    with gr.Row():
                        new_label = gr.Textbox(label="New Label", placeholder="New Label")
                        add_label = gr.Button("Add Label")
                        add_label.click(fn=add_group_label, inputs=[group_state, new_label], outputs=[group_state])

            with gr.Accordion("Group Images"):
                group_images = list_group_images(state, active_group)
                for image_name in group_images:
                    target_name = image_name
                    def select_image(state, image_name=target_name):
                        return view_image(image_name, state)

                    # label = path.basename(image)
                    image = gr.Image(image_name) # , label=label)
                    image.select(fn=select_image, inputs=[dataset_state], outputs=[dataset_state])

    return tab_group
