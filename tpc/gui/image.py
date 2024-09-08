import gradio as gr

with gr.Blocks() as tab_image:
    gr.Markdown("### Image")
    with gr.Row():
        image_path = gr.Textbox(label="Image Path", placeholder="path/to/image.jpg")
