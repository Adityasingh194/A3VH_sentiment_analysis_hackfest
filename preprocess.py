import re

def preprocessing_data(text):
    # Convert the entire tweet to lowercase
    text = text.lower()

    # Remove all hashtags at the end of the sentence (e.g., "#tag1 #tag2" at the end)
    text = re.sub(r'(?:#\w+\s*)+$', '', text)

    # Replace hashtags in the middle of the sentence with just the word (e.g., "#hello" → "hello")
    text = re.sub(r'#(\w+)', r'\1', text)

    # Remove Twitter mentions (e.g., "@username")
    text = re.sub(r'@\w+', '', text)

    # Remove URLs (http, https, or www links)
    text = re.sub(r'http\S+|www.\S+', '', text)

    # Remove all punctuation characters (e.g., ".", "!", "?", etc.)
    text = re.sub(r'[^\w\s]', '', text)

    # Remove all numeric digits
    text = re.sub(r'\d+', '', text)

    # Replace newline characters with space
    text = re.sub(r'\n+', ' ', text)

    # Remove any extra whitespace (multiple spaces → one space, and trim ends)
    text = re.sub(r'\s+', ' ', text).strip()

    # Return the cleaned tweet
    return text

def preprocess(df):
    df['cleaned_tweet'] = df['Content'].apply(preprocessing_data)
    return df
