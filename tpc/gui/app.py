import gradio as gr

from .dataset import tab_dataset

def image_classifier(image):
    return "label"

tab_group = gr.Interface(fn=image_classifier, inputs="image", outputs="label")

app = gr.TabbedInterface([tab_dataset, tab_group], ["Dataset", "Group"])
