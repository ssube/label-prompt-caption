import gradio as gr

from .dataset import make_dataset_tab
from .group import make_group_tab
from .image import make_image_tab

with gr.Blocks(title="LPC Studio") as app:
    app_state = gr.State()
    group_state = gr.State()

    gr.Markdown("# Label-Prompt-Caption Studio")

    with gr.Tab("Dataset"):
        make_dataset_tab(app_state)

    with gr.Tab("Group"):
        make_group_tab(app_state, group_state)

    with gr.Tab("Image"):
        make_image_tab(app_state, group_state)
