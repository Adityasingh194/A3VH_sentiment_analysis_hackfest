import os
import glob
import pandas as pd
import time
from concurrent.futures import (ThreadPoolExecutor,
                                ProcessPoolExecutor,
                                as_completed)
from pathlib import Path
from csv_deleter import csv_deleter
from sentiment_model import TextProcessor
from data_processing.prepocess import preprocess
from SentenceClustering import SentenceClustering
from ntfy import notification

def normalize_path(path):
    return path.replace("\\", "/")

folder_path = "C:/Users/Hemant Pathak/OneDrive/Desktop/chill/twitter_scrapper/tweets"
event = "modiji"

def scrape_tweets():
    print("[Scraping] Started...")
    csv_deleter()
    os.system(f"python scraper -ht {event} -t 10 --latest")

    # Wait for new file
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csv_files:
        print("[Scraping] No CSV found.")
        return None

    csv_files.sort(key=os.path.getmtime, reverse=True)
    latest_file = csv_files[0]
    print(f"[Scraping] Finished. File: {latest_file}")
    return latest_file


def process_sentiment(csv_file):
    print("[Sentiment] Processing:", csv_file)
    df = pd.read_csv(normalize_path(csv_file))
    df = preprocess(df)

    analyser = TextProcessor()
    df['sentiment'] = df['Content'].apply(lambda x: analyser.analyze_sentiment(x))

    print("[Sentiment] Done.")
    return df

def cluster_and_notify(df):
    print("[Clustering] Starting...")

    negative_sentences = df[df['sentiment'] == 'Negative']['Content'].tolist()

    if not negative_sentences:
        print("[Clustering] No negative sentences found.")
        return

    clustering = SentenceClustering()
    clustering.encode_sentences(negative_sentences)
    clustering.cluster_sentences()
    representatives = clustering.get_representative_sentences()

    for i in representatives:
        print(i)

    for sentence in representatives:
        notification(sentence)
    print("[Notify] Sent alerts.")

def pipeline():
    file=scrape_tweets()
    df=process_sentiment(file)
    cluster_and_notify(df)

    print(df['sentiment'])
pipeline()



