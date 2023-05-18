from transformers import AutoTokenizer, TFRobertaForMaskedLM
import tensorflow as tf
import string

tokenizer = AutoTokenizer.from_pretrained("EternalRecursion/roberta-finetuned-poetry")
model = TFRobertaForMaskedLM.from_pretrained("EternalRecursion/roberta-finetuned-poetry")

punctuation_ids = [tokenizer.encode(p)[1] for p in string.punctuation if len(tokenizer.encode(p)) == 3]  # Single-char tokens are encoded to 3 tokens


# def predict_mask(text, n=5, include_punctuation=False):
#     inputs = tokenizer(text, return_tensors="tf")
#     predictions = model(inputs)[0]
#     mask_token_index = tf.where(inputs["input_ids"][0] == tokenizer.mask_token_id)
#     mask_token_logits = predictions[0, mask_token_index[0][0], :]
#     mask_token_probs = tf.nn.softmax(mask_token_logits, axis=-1)

#     # Get all possible tokens and their probabilities
#     all_token_ids = tf.range(mask_token_probs.shape[-1])
#     all_token_probs = mask_token_probs.numpy()

#     # Filter out punctuation tokens, if requested
#     if not include_punctuation:
#         punctuation_ids = [tokenizer.encode(p)[1] for p in string.punctuation if len(tokenizer.encode(p)) == 3]  # Single-char tokens are encoded to 3 tokens
#         non_punctuation_indices = [i for i in range(len(all_token_probs)) if i not in punctuation_ids]
#         all_token_ids = tf.gather(all_token_ids, non_punctuation_indices)
#         all_token_probs = all_token_probs[non_punctuation_indices]

#     # Select top-k tokens
#     top_tokens = tf.math.top_k(all_token_probs, k=n)
#     top_token_ids = top_tokens.indices.numpy()
#     top_token_probs = top_tokens.values.numpy()
#     return list(zip([tokenizer.decode([token_id]) for token_id in top_token_ids], map(float, top_token_probs)))

def predict_mask(text, n=5, include_punctuation=False):
    inputs = tokenizer(text, return_tensors="tf")
    predictions = model(inputs)[0]
    mask_token_index = tf.where(inputs["input_ids"][0] == tokenizer.mask_token_id)
    mask_token_logits = predictions[0, mask_token_index[0][0], :]
    mask_token_probs = tf.nn.softmax(mask_token_logits, axis=-1)

    if not include_punctuation:
        mask = tf.constant([False if i in punctuation_ids else True for i in range(mask_token_probs.shape[0])])
        mask_token_probs = tf.where(mask, mask_token_probs, -tf.float32.max)

    top_tokens = tf.math.top_k(mask_token_probs, n)
    top_token_ids = top_tokens.indices.numpy()
    top_token_probs = top_tokens.values.numpy()
    return list(zip([tokenizer.decode([token_id]) for token_id in top_token_ids], map(float, top_token_probs)))



if __name__=="__main__":
    ## Testing
    print(predict_mask("I love to <mask>"))
    print(predict_mask("Paris is the capital of <mask>"))
    print(predict_mask("<mask> is the capital of Italy."))
    ## Measure speed
    import time
    start = time.time()
    for i in range(100):
        predict_mask("Paris is the capital of <mask>")
    print(time.time() - start)
