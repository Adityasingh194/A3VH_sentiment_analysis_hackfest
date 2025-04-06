Real-time Feedback Sentiment Analysis and Alert System
This project is built to help organizations monitor public sentiment and emerging issues during events by analyzing real-time feedback. The system collects data from multiple sources, processes it using machine learning models, and generates alerts for negative feedback patterns—all visualized on a live dashboard.

1. Project Overview
We developed a full-stack pipeline that:

Collects user feedback from multiple online platforms (e.g., social media, app chat, feedback forms)

Analyzes the sentiment of each message using a powerful ML model

Detects patterns in negative feedback to surface trending issues

Generates alerts in real-time using the NTFY application

Displays insights using a lightweight web dashboard

2. Why This Project?
Event managers and system admins often face delays in recognizing emerging problems.

This tool enables real-time monitoring so that problems like overcrowding or system failure can be quickly detected and resolved.

It helps in understanding user emotions and pain points based on large-scale unstructured text data.

3. System Workflow

Step-by-step Process:
Data Collection/Scraping:

Sources: Twitter, feedback forms, and in-app chat

Method: Selenium used instead of official APIs (APIs were paid or rate-limited)

Data Preprocessing:

Removed hashtags, mentions, digits, punctuation, and extra spaces

Replaced newlines with single space for consistency

Sentiment Analysis:

Used Gemma 3 (1B parameters) pre-trained model

Output is classified as Positive, Neutral, or Negative

Issue Detection:

Applied embedding + clustering techniques on negative feedback

Helps identify recurring or trending issues (e.g., delays, bugs, overcrowding)

Alert Generation:

Triggered via NTFY, a free and flexible notification service

Web Deployment:

Real-time dashboard updates using WebSockets

Hosted with Node.js, Express, and FastAPI backend

4. Key Technologies & Why We Chose Them
Component	Tool/Framework	Why This Was Selected
UI Dashboard	Streamlit	Simple, fast to build and update live charts
Backend API	FastAPI	Supports asynchronous processing; faster than Flask
Notification	NTFY	Lightweight, free, and ideal for custom alerts
Scraping	Selenium	Bypasses paid API restrictions of Twitter and others
Real-time Feed	WebSockets	Enables instant data push to the frontend
5. ML Models Compared
We experimented with several sentiment analysis models. Below is the performance summary:

Model	Accuracy (%)	Remarks
Naive Bayes	76	Fast but misses complex language patterns
SVM	79	Better pattern recognition, but slower
VADER	66	Rule-based, weak on context and sarcasm
VADER + BERT (Hybrid)	84	Improved sarcasm detection, moderate speed
BERT-base	80	Context-aware, but underperforms on sarcasm
RoBERTa-base	81	Slightly better sarcasm handling
Gemma 3 (1B)	94	Best performance on sarcasm, speed, and accuracy
6. Evaluation Criteria
We evaluated all models based on the following:

Macro F1-Score: Ensures balanced performance across all classes

Sarcasm Detection: Accuracy tested on manually labeled sarcastic sentences

Latency: Prediction time per input on CPU (important for real-time)

Ease of Integration: Ability to plug into production-grade systems

7. Real-time Deployment
The backend is deployed using FastAPI and Node.js

Real-time alerts and updates are enabled through WebSockets

Frontend dashboard built using Streamlit and deployed locally or globally

Feedback is continuously processed and reflected in the dashboard for organizers

8. Notes
Twitter and other APIs were avoided due to pricing; Selenium provided a free alternative.

NTFY was selected due to its flexibility, free license, and ease of setup.

All tools and libraries used are open-source and well-documented.
