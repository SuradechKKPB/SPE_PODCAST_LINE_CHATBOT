# SPE Podcast Recommendation LINE Bot

This project is a LINE chatbot that recommends SPE (Society of Petroleum Engineers) podcast episodes based on user interests using NLP and clustering. It runs locally using Flask and responds to real-time messages from LINE.

<img width="874" alt="Screenshot 2568-05-06 at 23 57 08" src="https://github.com/user-attachments/assets/67586942-9450-4c99-9038-42e8de2ec236" />


---

## 📌 Features
- Transcribes podcast audio using Whisper
- Clusters transcripts by topic with TF-IDF + KMeans
- Recommends podcast episodes based on keyword input
- LINE chatbot integration via Messaging API
- Local deployment with public exposure via Cloudflare Tunnel

---

## 📁 Project Structure
```
SPE-LINE-Bot/
├── main.py                       # Flask app that connects to LINE API
├── spe_llm_chatbot_nlp.py       # NLP analysis and recommendation engine
├── requirements.txt             # Python dependencies
├── README.md                    # Project overview and usage instructions
├── app.env.example              # Example for environment variable file
├── models/
│   └── ggml-model-q4.bin        # (Optional) Local LLM model file
├── credentials/
│   └── audiotranscriber-XXXX.json  # Google Sheets API credentials
└── data/
    └── sample_transcripts.csv   # Example dataset (optional)
```

---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/SuradechKKPB/SPE_PODCAST_LINE_CHATBOT.git
cd SPE_PODCAST_LINE_CHATBOT
```

### 2. Set up Python environment
```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Configure secrets
Create an `.env` file (or set environment variables manually):
```
LINE_TOKEN=your_long_lived_channel_access_token
LINE_SECRET=your_line_channel_secret
```
Place your Google API credentials in `credentials/audiotranscriber-XXXX.json`

---

## 🚀 Run the Application Locally
```bash
python main.py
```

### Expose your local server to LINE using Cloudflare Tunnel:
```bash
cloudflared tunnel --url http://localhost:8080
```

Use the given public HTTPS URL in the LINE Developer Console webhook.

---

## 🤖 How It Works
- Users send a topic (e.g., "automation") via LINE
- The app matches it against clustered transcript keywords
- It returns podcast titles that align with the user’s interests

---

## 📊 Technologies Used
- Python 3.10
- Flask
- LINE Messaging API
- Whisper (transcription)
- scikit-learn (TF-IDF, KMeans)
- gspread + Google Sheets
- llama-cpp-python (optional local LLM)
- Cloudflare Tunnel

---

## 📈 Future Improvements
- Multilingual support (Thai → English translation)
- Integration with Spotify/YouTube links
- Better clustering with SBERT or BERTopic
- Deployment on Google Cloud or Render

---

## 📄 License
MIT License.

---

## 🙌 Acknowledgments
Thanks to the Society of Petroleum Engineers (SPE) for podcast content and the open-source community for Whisper, LINE SDK, and Python libraries.

---

For any questions or contributions, feel free to open an issue or submit a pull request.
