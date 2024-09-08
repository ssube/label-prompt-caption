import gradio as gr

from .dataset import make_dataset_tab
from .group import tab_group
from .image import tab_image

with gr.Blocks() as app:
    state = gr.State()

    with gr.Tab("Dataset"):
        make_dataset_tab(state)

    gr.Tab("Group", tab_group)
    gr.Tab("Image", tab_image)
