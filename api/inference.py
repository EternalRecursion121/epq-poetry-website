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
