import gradio as gr

def make_image_tab(datset_state: gr.State):
    with gr.Blocks() as tab_image:
        gr.Markdown("### Image")
        with gr.Row():
            image_path = gr.Textbox(label="Image Path", placeholder="path/to/image.jpg")

    return tab_image
