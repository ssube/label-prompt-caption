# Label-Prompt-Caption Studio

## What

This is a Gradio UI for captioning small to medium-size datasets containing hundreds to thousands of images using
natural language and keyword/tag captioning models.

The name describes the captioning method:

1. Labels are applied to each image by humans or AI, describing critical details
2. A prompt is created for each image using a template and the image's labels
3. The prompt is passed to Florence, Joy, or another captioning model

## Why

Using labels to describe critical details and passing those labels on to the prompt helps the captioning model to
avoid mistakes and hallucinations.

Mistakes in the captions can cause problems later during training, especially if large or focal details are
mis-identified. Providing additional detail in the prompt can also help the captioning model to identify concepts it
is not familiar with.

## How

The required labels are defined for each group, along with templates for the image caption and templates for each
captioning model's prompt. The image labels are used to format those templates, providing more information to the
captioning models.

### Setup

Clone this repository:

```shell
> git clone git@github.com:ssube/label-prompt-caption.git
```

Set up a virtual environment:

```shell
> python3 -m venv venv
```

Install the requirements in the virtual environment:

```shell
> source venv/bin/activate
> pip3 install -r requirements.txt
```

### Usage

Using the virtual environment, run the server:

```shell
> source venv/bin/activate
> python3 -m lpc
```

Open the web UI in your browser. A link to the web UI will be shown in the logs, usually http://127.0.0.1:7860/.

1. On the `Dataset` tab, enter the `Base Path` for your dataset.
   1. This is the top-level directory which contains all of the images and group sub-directories.
2. Press the `Load Groups` button
   1. This will scan the dataset directory for images matching the `Image Formats`
3. Press the `View Group` button next to a group
4. Switch to the `Group` tab
5. Press the `Load Group` button
   1. This will load four additional sections: `Group Captions`, `Group Prompts`, `Group Taxonomy`, and `Group Images`
6. Provide a `Caption Template`
   1. You can use the template to add a prefix to every caption in the group, like `picture of {{ subject }}. {{ caption }}`
   2. The `{{ caption }}` variable will be set to the captioning model's output
7. Provide one or more `Group Prompts`
   1. For Florence, you can use one of `<CAPTION>`, `<DETAILED_CAPTION>`, or `<MORE_DETAILED_CAPTION>`
   2. For Joy, `Write a detailed description for this image of {{ subject }}.` is a good default but you can modify
      the prompt to include more details, the mood of the image, or any other helpful information.
8. Add any required labels to the `Group Taxonomy`
   1. These should include any variables in your `Caption Template` and `Group Prompts`, like `subject` in this example
   2. You do not need to include `caption` here
9. Select an image
10. Switch to the `Image` tab
11. Add annotations for any missing labels
    1. In this example, the `subject` might be a `dog`
12. The `Image Prompts` will show your `Group Prompts` templated with the labels and values from the image annotations
13. Press one of the `Caption with Florence` or `Caption with Joy` buttons
14. The `Image Caption` should update with a new caption describing your selected image
15. Modify the caption until it accurately describes the image
    1. The `Shuffle Phrases` button will randomly shuffle each phrase, split on commas
    2. The `Remove Newlines` button will remove any newlines in the caption
    3. The `Strip Partial Phrases` button will remove any text after the last `.`, in case the captioning model returned
       an incomplete phrase at the end of the prompt
16. Press the `Save Image Caption` button to save the caption to a `.txt` file
