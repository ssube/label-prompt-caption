from PIL import Image
from re import sub

from ..args import MODEL_DEVICE, MODEL_FORMAT

model = None
processor = None

def load_florence(model_name="microsoft/Florence-2-large-ft"):
    global model, processor

    from transformers import AutoProcessor, AutoModelForCausalLM

    print(f"Loading Florence from {model_name}...")
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=MODEL_FORMAT, trust_remote_code=True).to(MODEL_DEVICE)
    processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)

def unload_florence():
    global model, processor

    del model
    del processor

def caption_with_florence(image_name: str, prompt: str) -> str:
    # The task prompt is the leading <FOO> tag
    task_prompt = sub(r"<[A-Z]+>", "$1", prompt)
    image = Image.open(image_name)

    print("Captioning with Florence...", task_prompt, prompt, image)
    # return "A caption for the image using Florence"

    if not model or not processor:
        load_florence()

    inputs = processor(text=prompt, images=image, return_tensors="pt").to(MODEL_DEVICE, MODEL_FORMAT)
    generated_ids = model.generate(
      input_ids=inputs["input_ids"].to(MODEL_DEVICE),
      pixel_values=inputs["pixel_values"].to(MODEL_DEVICE),
      max_new_tokens=1024,
      early_stopping=False,
      do_sample=False,
      num_beams=3,
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed_answer = processor.post_process_generation(
        generated_text,
        task=task_prompt,
        image_size=(image.width, image.height)
    )

    if task_prompt not in parsed_answer:
        print(f"Reply for {task_prompt} not found in generated text {parsed_answer}")

    return parsed_answer[task_prompt]
