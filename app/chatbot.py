from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")
model = AutoModelForSeq2SeqLM.from_pretrained("microsoft/GODEL-v1_1-large-seq2seq")

# Global conversation memory (just last 3 messages for simplicity)
conversation_history = []

def get_bot_response(user_input):
    global conversation_history

    # Update history
    conversation_history.append(f"User: {user_input}")
    if len(conversation_history) > 6:
        conversation_history = conversation_history[-6:]  # Keep last 3 pairs

    dialog_context = " <|endoftext|> ".join(conversation_history) + " <|endoftext|>"

    prompt = (
        "Instruction: given a dialog context, respond empathetically.\n"
        f"Input: {dialog_context}\nOutput:"
    )

    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    outputs = model.generate(input_ids, max_length=150)

    bot_reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    conversation_history.append(f"Mira: {bot_reply}")

    return bot_reply.strip()
