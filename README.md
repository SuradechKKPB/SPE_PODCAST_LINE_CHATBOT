# SPE Podcast Recommendation LINE Bot

This project is a LINE chatbot that recommends SPE (Society of Petroleum Engineers) podcast episodes based on user interests using NLP and clustering. It runs locally using Flask and responds to real-time messages from LINE.

---
 
## 📌 Features
- Transcribes podcast audio using Whisper
- Clusters transcripts by topic with TF-IDF + KMeans
- Recommends podcast episodes based on keyword input
- LINE chatbot integration via Messaging API
- Local deployment with public exposure via Cloudflare Tunnel

---

## 📁 Project Structure
SPE-LINE-Bot/
├── main.py # Flask app that connects to LINE API
├── spe_llm_chatbot_nlp.py # NLP analysis and recommendation engine
├── requirements.txt # Python dependencies
├── README.md # Project overview and usage instructions
├── app.env.example # Example for environment variable file
├── models/
│ └── ggml-model-q4.bin 
├── credentials/
│ └── audiotranscriber-XXXX.json # Google Sheets API credentials
└── data/
└── sample_transcripts.csv 
