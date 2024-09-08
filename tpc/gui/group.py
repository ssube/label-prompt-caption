import gradio as gr
# from os import path

from models import AppState
from utils.dataset import list_group_images

def view_image(image: str, state: AppState) -> AppState:
    print("Viewing image...", image)
    new_state = AppState(**state.__dict__)
    new_state.active_image = image
    return new_state


def make_group_tab(dataset_state: gr.State):
    with gr.Blocks() as tab_group:
        gr.Markdown("Group stats, tag frequency, etc")

        @gr.render(inputs=[dataset_state])
        def render_group(state):
            active_group = state.active_group or "none"
            print("Rendering group...", active_group)

            with gr.Row():
                if state is None:
                    gr.Textbox(label="Group Name", value="none")
                    return

                gr.Textbox(label="Group Name", value=active_group)
                if state.active_group is None:
                    return

            with gr.Row():
                group_images = list_group_images(state, active_group)
                for image_name in group_images:
                    target_name = image_name
                    def select_image(state, image_name=target_name):
                        return view_image(image_name, state)

                    # label = path.basename(image)
                    image = gr.Image(image_name) # , label=label)
                    image.select(fn=select_image, inputs=[dataset_state], outputs=[dataset_state])

    return tab_group
