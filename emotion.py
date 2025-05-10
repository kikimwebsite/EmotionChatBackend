from transformers import pipeline

def run_and_display_nonzero_emotions(text, model_name="monologg/bert-base-cased-goemotions-original"):

    classifier = pipeline("text-classification", model=model_name, top_k=None)
    results = classifier(text)

    non_zero_emotions = [
        (emotion['label'], emotion['score'])
        for emotion in results[0]
        if emotion['score'] > 0.00
    ]

    sorted_emotions = sorted(non_zero_emotions, key=lambda x: x[1], reverse=True)

    return sorted_emotions