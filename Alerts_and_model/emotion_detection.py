from transformers import pipeline
classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier")
def emotion(text):
    results = classifier(text, top_k=3)
    return [res['label'] for res in results]

