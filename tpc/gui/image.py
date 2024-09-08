import gradio as gr

from models import AppState

def make_image_tab(dataset_state: gr.State):
    with gr.Blocks() as tab_image:
        gr.Markdown("Image stats, tag frequency, etc")

        @gr.render(inputs=[dataset_state])
        def render_image(state: AppState | None):
            if state is None or state.active_image is None:
                with gr.Row():
                    gr.Textbox(label="Image Path", placeholder="path/to/image.jpg")
                return

            with gr.Row():
                gr.Image(state.active_image)

    return tab_image
