from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed

def load_model(model_name: str = "deepseek1.3B", seed: int = 42):
    """
    Loads a text-generation model based on the provided model name.
    """
    match model_name:
        case 'deepseek1.3B':
            model = 'deepseek-ai/deepseek-coder-1.3b-instruct'
        case 'phi1.3B':
            model = 'microsoft/phi-1'
        case 'gptneo1.3B':
            model = 'EleutherAI/gpt-neo-1.3B'
        case 'fimneox1.3B':
            model = 'CarperAI/FIM-NeoX-1.3B'
        case 'nova1.3B':
            model = 'lt-asset/nova-1.3b-bcr'
        case 'mac_deepseek':
            model = 'TheBloke/deepseek-coder-1.3b-instruct-GGUF'
        case _:
            print(f"⚠️ Unknown model name '{model_name}'. Defaulting to DeepSeek 1.3B.")
            model = 'deepseek-ai/deepseek-coder-1.3b-instruct'

    print(f"🔧 Loading language model: {model} ...")

    # ✅ Load with trust_remote_code
    tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model, trust_remote_code=True)

    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    set_seed(seed)
    print(f"✅ Model '{model_id}' loaded successfully. Ready to chat.")
    return generator

def generate_response(generator, prompt: str, max_length: int = 100, temperature: float = 0.7, **kwargs):
    """
    Generates a response from the model using the given prompt.
    """
    if not prompt.strip():
        return "⚠️ Empty prompt provided."

    print("\n🤖 Felix is thinking...\n")
    response = generator(
        prompt,
        max_length=max_length,
        truncation=True,
        temperature=temperature,
        num_return_sequences=1,
        **kwargs
    )
    return response[0]['generated_text']
