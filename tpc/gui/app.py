import gradio as gr

from .dataset import tab_dataset
from .group import tab_group
from .image import tab_image

app = gr.TabbedInterface([tab_dataset, tab_group, tab_image], ["Dataset", "Group", "Image"])
