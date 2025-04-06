import os
import time
import shutil
import pandas as pd
import threading
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ml_app import SentenceClustering, extract_joined_phrase, TextProcessor,cluster_and_notify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_similarity
import spacy

UPLOAD_DIR = "uploads"
SAMPLE_DIR = "csv_samples"
sentiment_summary = {}
top_phrases = []
processor = None

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=[""], allow_headers=[""],
)

os.makedirs(UPLOAD_DIR, exist_ok=True)

# === Sentiment using RoBERTa ===

def preprocess(text):
    return str(text).strip().lower()

def process_csv(path):
    global sentiment_summary, top_phrases, processor
    print(f"Processing file: {path}")
    df = pd.read_csv(path)
    if "Content" not in df.columns:
        print(f"Skipping {path} due to missing 'Content' column")
        return

    df["cleaned"] = df["Content"].astype(str).apply(preprocess)
    df["sentiment"] = df["cleaned"].apply(lambda x: processor.analyze_sentiment(x))
    sentiment_summary = df["sentiment"].value_counts().to_dict()

    neg_df = df[df["sentiment"] == "Negative"]
    if not neg_df.empty:
        cluster = SentenceClustering()
        cluster.encode(neg_df["Content"].tolist())
        cluster.cluster()
        reps = cluster.get_representatives()
        top_phrases = extract_joined_phrase(reps)
    else:
        top_phrases = []

def repeat_csv_loop():
    global sentiment_summary, top_phrases
    while True:
        files = sorted(os.listdir(SAMPLE_DIR))
        for file in files:
            if file.endswith(".csv"):
                path = os.path.join(SAMPLE_DIR, file)
                df = pd.read_csv(path)

                if "Content" not in df.columns:
                    continue

                df["cleaned"] = df["Content"].astype(str).apply(preprocess)
                df["sentiment"] = df["cleaned"].apply(lambda x: processor.analyze_sentiment(x))

                sentiment_summary = df["sentiment"].value_counts().to_dict()

                # Cluster negative sentences
                neg_df = df[df["sentiment"] == "Negative"]
                if not neg_df.empty:
                    comments = neg_df["Content"].tolist()
                    cluster = SentenceClustering()
                    cluster.encode(comments)
                    cluster.cluster()
                    reps = cluster.get_representatives()
                    top_phrases = extract_joined_phrase(reps)
                else:
                    top_phrases = []

                print(f"Updated results for: {file}")
                time.sleep(30)

@app.on_event("startup")
def startup_event():
    global processor
    processor = TextProcessor()
    thread = threading.Thread(target=repeat_csv_loop, daemon=True)
    thread.start()

@app.post("/analyze")
async def analyze_csv(file: UploadFile = File(...)):
    global sentiment_summary, top_phrases

    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_csv(path)
    if "Content" not in df.columns:
        return {"error": "CSV must have 'Content' column"}

    df["cleaned"] = df["Content"].astype(str).apply(preprocess)
    df["sentiment"] = df["cleaned"].apply(lambda x: processor.analyze_sentiment(x))
    sentiment_summary = df["sentiment"].value_counts().to_dict()

    neg_df = df[df["sentiment"] == "Negative"]
    if not neg_df.empty:
        cluster = SentenceClustering()
        # cluster.encode(neg_df["Content"].tolist())
        # cluster.cluster()
        # reps = cluster.get_representatives()
        # top_phrases = extract_joined_phrase(reps)
        cluster_and_notify(df)
    else:
        top_phrases = []

    return {"status": "success", "sentiment_summary": sentiment_summary, "top_cluster_phrases": top_phrases}

@app.get("/latest_results")
def get_latest():
    return {
        "sentiment_summary": sentiment_summary,
        "top_cluster_phrases": top_phrases
    }