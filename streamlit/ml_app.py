import streamlit as st
import pandas as pd
import re
import requests
import spacy
import numpy as np
from transformers import pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# ---------------------- Text Processing & Sentiment Analysis ----------------------

class TextProcessor:
    def __init__(self, model_name="google/gemma-3-1b-it"):
        self.pipe = pipeline("text-generation", model=model_name, do_sample=False, top_k=1)

    def analyze_sentiment(self, text):
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

def preprocessing_data(text):
    text = text.lower()
    text = re.sub(r'(?:#\w+\s*)+$', '', text)
    text = re.sub(r'#(\w+)', r'\1', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'http\S+|www.\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess(df):
    df['cleaned_tweet'] = df['Content'].apply(preprocessing_data)
    return df

def process_sentiment(df):
    df = preprocess(df)
    analyser = TextProcessor()
    df['sentiment'] = df['cleaned_tweet'].apply(lambda x: analyser.analyze_sentiment(x))
    return df

# ---------------------- Clustering + Notification ----------------------

class SentenceClustering:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2', similarity_threshold=0.75, min_cluster_size=4):
        self.model = SentenceTransformer(model_name)
        self.similarity_threshold = similarity_threshold
        self.min_cluster_size = min_cluster_size

    def encode(self, sentences):
        self.sentences = sentences
        self.embeddings = self.model.encode(sentences)
        return self.embeddings

    def cluster(self):
        sim_matrix = cosine_similarity(self.embeddings)
        n = len(self.sentences)
        visited = [False] * n
        self.clusters = []

        def dfs(i, cluster):
            visited[i] = True
            cluster.append(i)
            for j in range(n):
                if not visited[j] and sim_matrix[i][j] >= self.similarity_threshold:
                    dfs(j, cluster)

        for i in range(n):
            if not visited[i]:
                cluster = []
                dfs(i, cluster)
                self.clusters.append(cluster)

    def get_representatives(self):
        representatives = []
        for cluster in self.clusters:
            if len(cluster) >= self.min_cluster_size:
                cluster_embeddings = [self.embeddings[i] for i in cluster]
                cluster_sentences = [self.sentences[i] for i in cluster]
                centroid = np.mean(cluster_embeddings, axis=0)
                similarities = cosine_similarity([centroid], cluster_embeddings)[0]
                rep_idx = np.argmax(similarities)
                representatives.append(cluster_sentences[rep_idx])
        return representatives
def extract_joined_phrase(sentences):
    if isinstance(sentences, str):
        sentences = [sentences]

    phrases = []
    for text in sentences:
        if isinstance(text, str):
            segments = re.split(r'[,.]', text)
            segments = [seg.strip() for seg in segments if len(seg.strip().split()) >= 2]
            phrases.extend(segments)

    # Get top 5 by length (or any custom logic)
    phrases = sorted(phrases, key=len, reverse=True)[:5]
    return phrases

def notification(data):
    try:
        resp = requests.post("https://ntfy.sh/BsObHxWEn4co6jW6", data=data.encode('utf-8'))
        print(f"Notification sent: {data} | Status code: {resp.status_code}")
    except Exception as e:
        print(f"Notification error: {e}")

def cluster_and_notify(df):
    negative_sentences = df[df['sentiment'] == 'Negative']['Content'].tolist()
    if not negative_sentences:
        return []

    clustering = SentenceClustering()
    clustering.encode(negative_sentences)
    clustering.cluster()
    representatives = clustering.get_representatives()
    phrases = extract_joined_phrase(representatives)

    for phrase in phrases:
        try:
            notification(phrase)
        except Exception as e:
            print(f"Notification error: {e}")
    
    return phrases
# ---------------------- Streamlit App ----------------------

import streamlit as st
import pandas as pd
import requests
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="📊 Live Sentiment Dashboard", layout="centered")
st.title("📡 Real-time Sentiment Monitoring")

# Auto-refresh every 30 seconds (in milliseconds)
st_autorefresh(interval=30 * 1000, key="datarefresh")

# Call FastAPI endpoint to get latest results
try:
    response = requests.get("http://127.0.0.1:8000/latest_results")
    data = response.json()["sentiment_summary"]

    if data:
        st.success("✅ Live Data Received!")
        st.bar_chart(data)
    else:
        st.warning("No sentiment data available yet. Waiting for CSV...")

except Exception as e:
    st.error(f"❌ Error fetching data: {e}")