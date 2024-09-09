import gradio as gr

from ..args import parse_args
from ..models import AppState
from .dataset import make_dataset_tab
from .group import make_group_tab
from .image import make_image_tab

args = parse_args()

def has_active_group(state: AppState | None):
    return state and state.active_group

def has_active_image(state: AppState | None):
    return state and state.active_image

with gr.Blocks(title="LPC Studio") as app:
    app_state = gr.State()
    group_state = gr.State()

    gr.Markdown("# Label-Prompt-Caption Studio")

    #@gr.render(inputs=[app_state])
    #def render_tabs(state: AppState | None):
    with gr.Tab("Dataset"):
        make_dataset_tab(args, app_state)

    with gr.Tab("Group", interactive=has_active_group(app_state.value)):
        make_group_tab(args, app_state, group_state)

    with gr.Tab("Image", interactive=has_active_image(app_state.value)):
        make_image_tab(args, app_state, group_state)
