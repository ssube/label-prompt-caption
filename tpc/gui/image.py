import gradio as gr
from jinja2 import Environment
from os import path

from args import CAPTION_MODELS
from caption_models import CAPTION_CALLBACKS
from models import AppState, GroupMetaFile, ImageMeta, AnnotationMeta
from utils.image import get_annotation_dict


jinja = Environment()


def add_image_annotation(group_meta: GroupMetaFile, image: str, label: str, value: str) -> GroupMetaFile:
    print("Adding image annotation...", label, value)
    image_meta = group_meta.images.get(image, ImageMeta())
    image_meta.annotations.append(AnnotationMeta(label=label, value=value))

    new_group_meta = GroupMetaFile(**group_meta.__dict__)
    new_group_meta.images[image] = image_meta
    return new_group_meta


def update_image_annotation(group_meta: GroupMetaFile, image: str, label: str, value: str) -> GroupMetaFile:
    print("Updating image annotation...", label, value)
    image_meta = group_meta.images.get(image, ImageMeta())
    for annotation in image_meta.annotations:
        if annotation.label == label:
            annotation.value = value

    new_group_meta = GroupMetaFile(**group_meta.__dict__)
    new_group_meta.images[image] = image_meta
    return new_group_meta


def caption_image(image: str, model: str, prompt: str) -> str:
    callback = CAPTION_CALLBACKS[model]
    caption = callback(image, prompt)
    print(f"Captioned image with {model}: {caption}")

    # TODO: apply group caption template
    return caption


def load_image_caption(image: str) -> str:
    caption_file = path.splitext(image)[0] + ".txt"

    try:
        with open(caption_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def save_image_caption(image: str, caption: str) -> None:
    caption_file = path.splitext(image)[0] + ".txt"

    with open(caption_file, "w") as f:
        f.write(caption)


def make_image_tab(dataset_state: gr.State, group_state: gr.State):
    with gr.Blocks() as tab_image:
        @gr.render(inputs=[dataset_state, group_state])
        def render_image(state: AppState | None, group_meta: GroupMetaFile | None):
            with gr.Row():
                if state is None or state.active_image is None:
                    gr.Markdown("No image selected")
                    return

                gr.Textbox(label="Image Path", value=state.active_image)

            image_caption = load_image_caption(state.active_image)
            image_meta = group_meta.images.get(state.active_image, ImageMeta())
            image_labels = {annotation.label for annotation in image_meta.annotations}

            required_labels = set(group_meta.group.required_labels)
            missing_labels = required_labels - image_labels

            with gr.Accordion("Image Annotations"):
                # flag missing required annotations
                if missing_labels:
                    with gr.Row():
                        gr.Label(f"Missing required labels: {', '.join(missing_labels)}", color="red")

                for annotation in image_meta.annotations:
                    with gr.Row():
                        def update_annotation(group_state, value):
                            return update_image_annotation(group_state, state.active_image, annotation.label, value)

                        elem = gr.Textbox(label=annotation.label, value=annotation.value, interactive=True, scale=3)
                        update = gr.Button("Update Annotation", scale=1)
                        update.click(fn=update_annotation, inputs=[group_state, elem], outputs=[group_state])

                with gr.Row():
                    def add_annotation(group_state, label, value):
                        return add_image_annotation(group_state, state.active_image, label, value)

                    label = gr.Textbox(label="Annotation Label", scale=1)
                    value = gr.Textbox(label="Annotation Value", scale=2)
                    add = gr.Button("Add Annotation", scale=1)
                    add.click(fn=add_annotation, inputs=[group_state, label, value], outputs=[group_state])

            with gr.Accordion("Image Caption"):
                with gr.Row():
                    caption = gr.Textbox(label="Image Caption", value=image_caption, interactive=True, scale=3)
                    set_caption = gr.Button("Save Image Caption", scale=1)
                    set_caption.click(fn=lambda caption: save_image_caption(state.active_image, caption), inputs=[caption])


            with gr.Accordion("Image Prompts"):
                for model in CAPTION_MODELS:
                    with gr.Row():
                        prompt_template = jinja.from_string(group_meta.group.prompt.get(model, "{{ caption }}"))
                        prompt_args = get_annotation_dict(image_meta)
                        prompt = prompt_template.render(**prompt_args, caption="{{ caption }}")
                        def on_caption(image=state.active_image, model=model, prompt=prompt):
                            print("Captioning with", image, model, prompt)
                            return caption_image(image, model, prompt)

                        gr.Textbox(label=model, value=prompt, scale=3)
                        do_caption = gr.Button(f"Caption with {model}", scale=1)
                        do_caption.click(fn=on_caption, outputs=[caption])

            with gr.Row():
                gr.Image(state.active_image, height=1024, width=1024)

    return tab_image
