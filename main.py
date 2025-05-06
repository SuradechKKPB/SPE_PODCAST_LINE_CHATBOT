
from flask import Flask, request, jsonify
import hashlib, hmac, base64, os, json, requests
from spe_llm_chatbot_nlp import run_nlp_analysis, get_recommendation

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "SPblETk9YnClR+cMu6sOI54OXCPZrbiEQAWVpkVdOnvt1rnMghgX0mlQFgc9IV5zaoVa9FZna6pQs45cciuyKnyrzXeLcBeRkNVuaW6+vWa8fSeCYqFAMebR2H7SnM4jKCtRmpYJcGXDY/V+RzwplQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "e3e2c5d3200f8df1ac79a788ed5a0886"

cluster_keywords = run_nlp_analysis()

def reply_to_line(reply_token, message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, data=json.dumps(payload))

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    print("Webhook received:", body)
    hash = hmac.new(LINE_CHANNEL_SECRET.encode(), body.encode(), hashlib.sha256).digest()
    computed = base64.b64encode(hash).decode()

    if not hmac.compare_digest(computed, signature):
        return "Invalid signature", 403

    events = request.json.get("events", [])
    for event in events:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_input = event["message"]["text"]
            reply_token = event["replyToken"]
            response = get_recommendation(user_input, cluster_keywords)
            reply_to_line(reply_token, response)
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "LINE bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
