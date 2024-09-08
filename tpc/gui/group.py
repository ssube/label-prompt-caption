import gradio as gr

def make_group_tab(dataset_state: gr.State):
    with gr.Blocks() as tab_group:
        gr.Markdown("### Group")
        refresh = gr.Button("Refresh")

        @gr.render(inputs=[dataset_state])
        def render_group(dataset_state):
            active_group = dataset_state.active_group or "none"
            print("Rendering group...", active_group)

            with gr.Row():
                if dataset_state is None:
                    gr.Textbox(label="Group Name", value="none")
                    return

                gr.Textbox(label="Group Name", value=active_group)

        refresh.click(fn=render_group, inputs=[dataset_state])

    return tab_group
