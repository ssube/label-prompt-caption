import gradio as gr

from args import CAPTION_MODELS
from models import AppState

def make_image_tab(dataset_state: gr.State):
    with gr.Blocks() as tab_image:
        gr.Markdown("Image stats, tag frequency, etc")

        @gr.render(inputs=[dataset_state])
        def render_image(state: AppState | None):
            with gr.Row():
                if state is None or state.active_image is None:
                    gr.Textbox(label="Image Path", placeholder="path/to/image.jpg")
                    return

                gr.Textbox(label="Image Path", value=state.active_image)

            with gr.Accordion("Image Annotations"):
                gr.Markdown("Image annotations, tags, etc")

            with gr.Accordion("Image Prompts"):
                for model in CAPTION_MODELS:
                    # TODO: format prompt using image annotations
                    gr.Textbox(label=model, placeholder=f"{model} prompt")

            with gr.Row():
                gr.Image(state.active_image, height=1024, width=1024)

    return tab_image
