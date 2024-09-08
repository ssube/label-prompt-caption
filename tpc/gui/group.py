import gradio as gr

with gr.Blocks() as tab_group:
    gr.Markdown("### Group")
    with gr.Row():
        group_name = gr.Textbox(label="Group Name", value="group1")
