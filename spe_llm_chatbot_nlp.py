import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from wordcloud import WordCloud
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from llama_cpp import Llama  # CPU-based LLM inference (optional)

# === CONFIG ===
SPREADSHEET_NAME = "Podcast Transcripts"
CREDENTIAL_FILE = "YOUR_CREDENTIAL_FILE.json"
GGML_MODEL_PATH = "./models/ggml-model-q4.bin"  # optional

# === Load Transcripts and Titles from Google Sheets ===
def load_transcripts_with_titles(spreadsheet_name=SPREADSHEET_NAME):
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIAL_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).sheet1
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    df = df.rename(columns=lambda x: x.strip())
    return df['Title'], df['Transript']  # Ensure columns match Google Sheet

# === Clean Text ===
def clean_text(text):
    return re.sub(r'[^A-Za-z0-9 ]+', '', text.lower())

# === Vectorize and Cluster ===
def analyze_clusters(texts, titles, num_clusters=5):
    cleaned = [clean_text(t) for t in texts]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(cleaned)

    model = KMeans(n_clusters=num_clusters, random_state=42)
    model.fit(X)

    labels = model.labels_
    score = silhouette_score(X, labels)
    print(f"Silhouette Score: {score:.2f}")

    # Extract top keywords and associated titles
    keywords = []
    cluster_titles = [[] for _ in range(num_clusters)]
    for i in range(num_clusters):
        cluster_center = model.cluster_centers_[i]
        terms = vectorizer.get_feature_names_out()
        top_terms = [terms[ind] for ind in cluster_center.argsort()[-10:][::-1]]
        keywords.append(top_terms)

    for idx, label in enumerate(labels):
        cluster_titles[label].append(titles[idx])

    return keywords, cluster_titles

# === Word Cloud Plot ===
def plot_wordclouds(texts):
    wc = WordCloud(width=800, height=400, background_color='white').generate(' '.join(texts))
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title("Podcast Word Cloud")
    plt.show()

# === Recommendation Function for Chatbot ===
def get_recommendation(user_input, cluster_keywords_titles, top_n=3):
    cluster_keywords, cluster_titles = cluster_keywords_titles
    user_input_lower = user_input.lower()
    scores = []
    for i, keywords in enumerate(cluster_keywords):
        match_count = sum(word in user_input_lower for word in keywords)
        scores.append((i, match_count))

    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    matched_clusters = [i for i, count in scores[:top_n] if count > 0]

    if matched_clusters:
        response = ["We analyzed our podcast database using NLP and clustered it by topic.",
                    f"Based on your interest in \"{user_input}\", you’ll likely enjoy:"]
        for idx in matched_clusters:
            cluster_desc = ", ".join(cluster_keywords[idx][:5])
            top_titles = cluster_titles[idx][:5]
            for title in top_titles:
                response.append(f"- {title} (Cluster {idx+1}: {cluster_desc})")
        return "\n".join(response)
    else:
        cluster_summary = [f"Cluster {i+1}: {', '.join(keywords[:5])}" for i, keywords in enumerate(cluster_keywords)]
        return ("We couldn’t find a strong match based on your input.\n"
                "Here’s how our podcast library is clustered:\n" + "\n".join(cluster_summary))

# === Optional: Load Local CPU-based LLM ===
def load_local_llm_cpu():
    return Llama(model_path=GGML_MODEL_PATH)

def query_local_llm_cpu(llm, text, prompt_template):
    prompt = prompt_template.format(text=text)
    output = llm(prompt, max_tokens=512, stop=["\n"])
    return output['choices'][0]['text'].strip()

# === Run NLP Pipeline ===
def run_nlp_analysis():
    titles, texts = load_transcripts_with_titles()
    keywords, cluster_titles = analyze_clusters(texts, titles)
    return keywords, cluster_titles
