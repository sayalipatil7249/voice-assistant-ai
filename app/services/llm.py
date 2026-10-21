from transformers import AutoTokenizer, AutoModelForCausalLM

# Open-source instruction-tuned LLM
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load model
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


def generate_response(text):
    # Convert user text into the format expected by the instruction-tuned model
    messages = [
        {
            "role": "user",
            "content": text
        }
    ]

    # Convert messages into model input tokens
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Convert text into Token IDs
    inputs = tokenizer(prompt, return_tensors="pt")

    # Generate response
    outputs = model.generate(
        **inputs,
        max_new_tokens=100
    )

    # Convert generated Token IDs back into readable text
    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    )

    return response