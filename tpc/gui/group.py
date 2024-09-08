import gradio as gr
from os import path

from utils.dataset import list_group_images

def make_group_tab(dataset_state: gr.State):
    with gr.Blocks() as tab_group:
        gr.Markdown("### Group")

        @gr.render(inputs=[dataset_state])
        def render_group(dataset_state):
            active_group = dataset_state.active_group or "none"
            print("Rendering group...", active_group)

            with gr.Row():
                if dataset_state is None:
                    gr.Textbox(label="Group Name", value="none")
                    return

                gr.Textbox(label="Group Name", value=active_group)
                if dataset_state.active_group is None:
                    return

            with gr.Row():
                group_images = list_group_images(dataset_state, active_group)
                for image in group_images:
                    # label = path.basename(image)
                    gr.Image(image) # , label=label)

    return tab_group
