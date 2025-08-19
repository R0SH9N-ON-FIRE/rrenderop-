from flask import Flask, request, render_template_string
import requests, datetime, os, pyttsx3

app = Flask(__name__)
os.makedirs("logs", exist_ok=True)

# 🔥 Rainbow Banner
def rainbow_banner(text):
    colors = ['\033[91m', '\033[93m', '\033[92m', '\033[96m', '\033[94m', '\033[95m']
    reset = '\033[0m'
    banner = ''.join(colors[i % len(colors)] + ch for i, ch in enumerate(text)) + reset
    print(banner)

rainbow_banner("🔥 DUBUNG MODE ACTIVATED 🔥")

# 🎙️ Voice Intro
engine = pyttsx3.init()
engine.say("Dubung mode activated. Server is live!")
engine.runAndWait()

# 📨 Message Sender
def send_message(token, recipient_id, message):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={token}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    res = requests.post(url, json=payload)
    log = f"{datetime.datetime.now()} | 📨 भेजा गया {recipient_id} को | {'✅ सफल' if res.ok else '⚠️ त्रुटि'}\n"
    with open("logs/message_log.txt", "a", encoding="utf-8") as f:
        f.write(log)
    return "✅ Message Sent!" if res.ok else f"⚠️ Error: " + res.text

# 🌐 Web UI (Inline)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🔥 Dubung Messenger</title>
    <style>
        body { font-family: sans-serif; background: linear-gradient(to right, #ff4e50, #f9d423); color: #222; padding: 20px; }
        h1 { text-align: center; color: white; text-shadow: 2px 2px #000; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input, textarea { width: 100%; padding: 10px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc; }
        button { margin-top: 15px; padding: 10px 20px; background: #222; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .status { margin-top: 20px; font-size: 18px; }
    </style>
</head>
<body>
    <h1>🔥 Dubung Messenger | डबंग संदेश सेवा</h1>
    <form method="POST">
        <label>🔑 Token (टोकन):</label>
        <input type="text" name="token" required>

        <label>👤 Recipient ID (प्राप्तकर्ता आईडी):</label>
        <input type="text" name="recipient" required>

        <label>💬 Message (संदेश):</label>
        <textarea name="message" rows="4" required></textarea>

        <button type="submit">📤 Send भेजें</button>
    </form>
    <div class="status">{{ status }}</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    status = ""
    if request.method == "POST":
        token = request.form["token"]
        recipient_id = request.form["recipient"]
        message = request.form["message"]
        status = send_message(token, recipient_id, message)
    return render_template_string(HTML_TEMPLATE, status=status)

app.run(host="0.0.0.0", port=81)
