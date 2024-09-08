import gradio as gr

from .dataset import make_dataset_tab
from .group import make_group_tab
from .image import make_image_tab

with gr.Blocks() as app:
    state = gr.State()

    with gr.Tab("Dataset"):
        make_dataset_tab(state)

    with gr.Tab("Group"):
        make_group_tab(state)

    with gr.Tab("Image"):
        make_image_tab(state)
