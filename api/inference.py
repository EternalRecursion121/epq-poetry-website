from transformers import AutoTokenizer, TFRobertaForMaskedLM
import tensorflow as tf

tokenizer = AutoTokenizer.from_pretrained("EternalRecursion/roberta-finetuned-poetry")
model = TFRobertaForMaskedLM.from_pretrained("EternalRecursion/roberta-finetuned-poetry")

def predict_mask(text, n=5):
    inputs = tokenizer(text, return_tensors="tf")
    predictions = model(inputs)[0]
    mask_token_index = tf.where(inputs["input_ids"][0] == tokenizer.mask_token_id)
    mask_token_logits = predictions[0, mask_token_index[0][0], :]
    mask_token_probs = tf.nn.softmax(mask_token_logits, axis=-1)
    top_tokens = tf.math.top_k(mask_token_probs, n)
    top_token_ids = top_tokens.indices.numpy()
    top_token_probs = top_tokens.values.numpy()
    return list(zip([tokenizer.decode([token_id]) for token_id in top_token_ids], top_token_probs))





