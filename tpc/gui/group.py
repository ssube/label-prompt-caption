import gradio as gr
# from os import path

from args import Args
from models import AppState, GroupMetaFile
from utils.dataset import list_group_images
from utils.group import count_group_labels, load_group_meta, save_group_meta

def view_image(image: str, state: AppState) -> AppState:
    print("Viewing image...", image)
    new_state = AppState(**state.__dict__)
    new_state.active_image = image
    return new_state


def add_group_label(group_state: GroupMetaFile, label: str) -> GroupMetaFile:
    print("Adding label...", label)
    new_group_state = GroupMetaFile(**group_state.__dict__)
    new_group_state.group.required_labels.append(label)
    return new_group_state


def remove_group_label(group_state: GroupMetaFile, label: str) -> GroupMetaFile:
    print("Removing label...", label)
    new_group_state = GroupMetaFile(**group_state.__dict__)
    new_group_state.group.required_labels.remove(label)
    return new_group_state


def set_group_caption(group_state: GroupMetaFile, caption: str) -> GroupMetaFile:
    print("Setting caption...", caption)
    new_group_state = GroupMetaFile(**group_state.__dict__)
    new_group_state.group.caption = caption
    return new_group_state


def set_group_prompt(group_state: GroupMetaFile, model: str, prompt: str) -> GroupMetaFile:
    print("Setting prompt...", model, prompt)
    new_group_state = GroupMetaFile(**group_state.__dict__)
    new_group_state.group.prompt[model] = prompt
    return new_group_state


def load_group_state(dataset_state: AppState, group: str | None = None) -> GroupMetaFile:
    if group is None:
        group = get_active_or_first_group(dataset_state)

    print("Loading group state...", group)
    group_meta = load_group_meta(dataset_state.dataset, group)
    return group_meta


def save_group_state(dataset_state: AppState, group_state: GroupMetaFile) -> None:
    print("Saving group state...", dataset_state.active_group, group_state)
    save_group_meta(dataset_state.dataset, dataset_state.active_group, group_state)


def get_active_or_first_group(state: AppState | None) -> str | None:
    if state is None:
        return None

    if state.active_group:
        return state.active_group

    if len(state.groups):
        return state.groups[0]

    return None


def make_group_tab(args: Args, dataset_state: gr.State, group_state: gr.State):
    with gr.Blocks() as tab_group:
        @gr.render(inputs=[dataset_state, group_state])
        def render_group(state: AppState | None, group_meta: GroupMetaFile | None):
            active_group = get_active_or_first_group(state)

            if state is None or active_group is None:
                with gr.Row():
                    gr.Textbox(label="Group Name", value="none")
                    return

            print("Rendering group...", active_group)

            with gr.Row():
                gr.Button("Previous Group", scale=1, interactive=False)
                gr.Textbox(label="Group Name", value=active_group, scale=4)
                gr.Button("Next Group", scale=1, interactive=False)

            with gr.Row():
                load = gr.Button("Load Group Meta")
                load.click(fn=load_group_state, inputs=[dataset_state], outputs=[group_state])
                save = gr.Button("Save Group Meta")
                save.click(fn=save_group_state, inputs=[dataset_state, group_state])

            if not group_meta:
                gr.Markdown("### No group metadata loaded.")
                return
                # group_meta = load_group_state(state, active_group)

            with gr.Accordion("Group Captions"):
                with gr.Row():
                    caption = gr.Textbox(label="Caption Template", value=group_meta.group.caption, interactive=True, scale=3)
                    set_caption = gr.Button("Set Caption Template", scale=1)
                    set_caption.click(fn=lambda c: set_group_caption(group_meta, c), inputs=[caption], outputs=[group_state])

                with gr.Row():
                    for model in args.caption_models:
                        gr.Button(f"Caption group with {model}", interactive=False)

            with gr.Accordion("Group Prompts"):
                for model in args.caption_models:
                    with gr.Row():
                        def set_prompt(prompt, model=model, state=group_meta):
                            return set_group_prompt(state, model, prompt)

                        prompt = gr.Textbox(label=model, placeholder=f"{model} prompt", scale=3, value=group_meta.group.prompt.get(model, ""))
                        gr.Button(f"Set {model} Prompt", scale=1).click(fn=set_prompt, inputs=[prompt], outputs=[group_state])

            with gr.Accordion("Group Taxonomy"):
                if len(group_meta.group.required_labels):
                    gr.Markdown("### Required Labels")
                    for required_label in group_meta.group.required_labels:
                        with gr.Row():
                            label = gr.Textbox(label="Required Label", scale=3, value=required_label)
                            remove_label = gr.Button("Remove Required Label", scale=1)
                            remove_label.click(fn=lambda l: remove_group_label(group_meta, l), inputs=[label], outputs=[group_state])

                with gr.Row():
                    new_label = gr.Textbox(label="New Label", placeholder="New Label", scale=3)
                    add_label = gr.Button("Add Required Label", scale=1)
                    add_label.click(fn=lambda l: add_group_label(group_meta, l), inputs=[new_label], outputs=[group_state])

                with gr.Row():
                    group_labels = count_group_labels(group_meta)
                    gr.Dataframe(
                        headers=["Label", "Count", "Required"],
                        value=[[label, count, label in group_meta.group.required_labels] for label, count in group_labels.items()],
                    )

            with gr.Accordion("Group Images"):
                group_images = list_group_images(state, active_group)
                with gr.Row():
                    for image_name in group_images:
                        target_name = image_name
                        def select_image(state, image_name=target_name):
                            return view_image(image_name, state)

                        # label = path.basename(image)
                        image = gr.Image(image_name) # , label=label)
                        image.select(fn=select_image, inputs=[dataset_state], outputs=[dataset_state])

    return tab_group
