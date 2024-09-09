from PIL import Image
from torch import nn
from os import environ
import torch

from args import MODEL_DEVICE, MODEL_FORMAT

CLIP_MODEL = "google/siglip-so400m-patch14-384"
LLAMA_FREE = "cognitivecomputations/dolphin-2.9.4-llama3.1-8b"
LLAMA_GATED = "meta-llama/Meta-Llama-3.1-8B"
LLAMA_MODEL = environ.get("LPC_LLAMA_MODEL", LLAMA_GATED)

class ImageAdapter(nn.Module):
    def __init__(self, input_features: int, output_features: int):
        super().__init__()
        self.linear1 = nn.Linear(input_features, output_features)
        self.activation = nn.GELU()
        self.linear2 = nn.Linear(output_features, output_features)

    def forward(self, vision_outputs: torch.Tensor):
        x = self.linear1(vision_outputs)
        x = self.activation(x)
        x = self.linear2(x)
        return x

clip_model = None
clip_processor = None
image_adapter = None
llama_model = None
llama_tokenizer = None

def load_joy(clip_name=CLIP_MODEL, model_name=LLAMA_MODEL):
    global clip_model, clip_processor, image_adapter, llama_model, llama_tokenizer

    from huggingface_hub import hf_hub_download
    from transformers import AutoModel, AutoProcessor, AutoTokenizer, PreTrainedTokenizer, PreTrainedTokenizerFast, AutoModelForCausalLM

    print("Loading CLIP")
    clip_processor = AutoProcessor.from_pretrained(clip_name)
    clip_model = AutoModel.from_pretrained(clip_name)
    clip_model = clip_model.vision_model
    clip_model.eval()
    clip_model.requires_grad_(False)
    clip_model.to(MODEL_DEVICE)

    # Tokenizer
    print("Loading tokenizer")
    llama_tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    assert isinstance(llama_tokenizer, PreTrainedTokenizer) or isinstance(llama_tokenizer, PreTrainedTokenizerFast), f"Tokenizer is of type {type(llama_tokenizer)}"

    # LLM
    print("Loading LLM")
    llama_model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=MODEL_FORMAT) # TODO: support bfloat16
    llama_model.eval()

    # Image Adapter
    print("Loading image adapter")
    adapter_path = hf_hub_download("fancyfeast/joy-caption-pre-alpha", subfolder="wpkklhc6", filename="image_adapter.pt", repo_type="spaces")
    image_adapter = ImageAdapter(clip_model.config.hidden_size, llama_model.config.hidden_size)
    image_adapter.load_state_dict(torch.load(adapter_path, map_location="cpu"))
    image_adapter.eval()
    image_adapter.to(MODEL_DEVICE)


@torch.no_grad()
def caption_with_joy(image_name: str, prompt: str) -> str:
    image = Image.open(image_name)
    print("Captioning with Joy...", prompt, image)
    # return "A caption for the image using Joy"

    if not clip_model or not clip_processor or not image_adapter or not llama_model or not llama_tokenizer:
        load_joy()

    torch.cuda.empty_cache()

    # Preprocess image
    image = clip_processor(images=image, return_tensors='pt').pixel_values
    image = image.to(MODEL_DEVICE)

    # Tokenize the prompt
    prompt = llama_tokenizer.encode(prompt, return_tensors='pt', padding=False, truncation=False, add_special_tokens=False)

    # Embed image
    with torch.amp.autocast_mode.autocast(MODEL_DEVICE, enabled=True):
        vision_outputs = clip_model(pixel_values=image, output_hidden_states=True)
        image_features = vision_outputs.hidden_states[-2]
        embedded_images = image_adapter(image_features)
        embedded_images = embedded_images.to(MODEL_DEVICE)

    # Embed prompt
    prompt_embeds = llama_model.model.embed_tokens(prompt.to(MODEL_DEVICE))
    assert prompt_embeds.shape == (1, prompt.shape[1], llama_model.config.hidden_size), f"Prompt shape is {prompt_embeds.shape}, expected {(1, prompt.shape[1], llama_model.config.hidden_size)}"
    embedded_bos = llama_model.model.embed_tokens(torch.tensor([[llama_tokenizer.bos_token_id]], device=llama_model.device, dtype=torch.int64))

    # Construct prompts
    inputs_embeds = torch.cat([
        embedded_bos.expand(embedded_images.shape[0], -1, -1),
        embedded_images.to(dtype=embedded_bos.dtype),
        prompt_embeds.expand(embedded_images.shape[0], -1, -1),
    ], dim=1)

    input_ids = torch.cat([
        torch.tensor([[llama_tokenizer.bos_token_id]], dtype=torch.long),
        torch.zeros((1, embedded_images.shape[1]), dtype=torch.long),
        prompt,
    ], dim=1).to(MODEL_DEVICE)
    attention_mask = torch.ones_like(input_ids)

    generate_ids = llama_model.generate(input_ids, inputs_embeds=inputs_embeds, attention_mask=attention_mask, max_new_tokens=300, do_sample=True, top_k=10, temperature=0.5, suppress_tokens=None)

    # Trim off the prompt
    generate_ids = generate_ids[:, input_ids.shape[1]:]
    if generate_ids[0][-1] == llama_tokenizer.eos_token_id:
        generate_ids = generate_ids[:, :-1]

    caption = llama_tokenizer.batch_decode(generate_ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)[0]
    caption = caption.replace("<|end_of_text|>", "").strip()
    return caption
