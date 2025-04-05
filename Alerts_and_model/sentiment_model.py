from transformers import pipeline
import re
import torch
import gc
import time


class TextProcessor:
    def __init__(self, model_name="google/gemma-3-1b-it"):
        """
        Initialize the text generation pipeline once to reduce loading overhead.
        """
        self.model_name = model_name
        self.pipe = pipeline("text-generation", model=self.model_name, do_sample=False, top_k=1)

    def translate(self, text):
        """
        Translate Hinglish to English using a prompt-style system message.
        """
        messages = [[
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful text translator that translates text from hinglish to english"}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": text}]
            }
        ]]

        output = self.pipe(messages, max_new_tokens=50)
        assistant_content = output[0][0]['generated_text'][-1]['content']

        match = re.search(r'\*\*"(.+?)"\*\*', assistant_content)
        if match:
            return match.group(1)
        else:
            return assistant_content  # Fallback if formatting doesn't match

    def analyze_sentiment(self, text):
        """
        Perform sentiment analysis by asking the model to classify the sentiment.
        """
        messages = [[
            {
                "role": "system",
                "content": [{"type": "text", "text": "You are a helpful text classifier into positive, negative and neutral classes"}]
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": text}]
            }
        ]]

        output = self.pipe(messages, max_new_tokens=1)
        sentiment = output[0][0]['generated_text'][-1]['content']
        return sentiment