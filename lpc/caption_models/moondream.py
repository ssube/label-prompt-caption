from PIL import Image

from ..args import MODEL_DEVICE

model = None
tokenizer = None

def load_moondream(model_name="vikhyatk/moondream2", revision="main"):
    global model, tokenizer

    from transformers import AutoModelForCausalLM, AutoTokenizer

    model = AutoModelForCausalLM.from_pretrained(
        model_name, trust_remote_code=True, revision=revision
    ).to(MODEL_DEVICE)
    tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)


def unload_moondream():
    global model, tokenizer

    del model
    del tokenizer


def caption_with_moondream(image_name: str, prompt: str) -> str:
    image = Image.open(image_name)
    print("Captioning with Moondream...", prompt, image)

    image_embeds = model.encode_image(image)
    caption = model.answer_question(image_embeds, prompt, tokenizer)
    return caption
