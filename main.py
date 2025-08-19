from flask import Flask, render_template, request
import requests, datetime, os

app = Flask(__name__)
os.makedirs("logs", exist_ok=True)

def send_message(token, recipient_id, message):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={token}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    res = requests.post(url, json=payload)
    log = f"{datetime.datetime.now()} | 📨 Sent to {recipient_id} | {'✅' if res.ok else '⚠️'}\n"
    with open("logs/message_log.txt", "a") as f:
        f.write(log)
    return "✅ Message Sent!" if res.ok else f"⚠️ Error: " + res.text

@app.route("/", methods=["GET", "POST"])
def home():
    status = ""
    if request.method == "POST":
        token = request.form["token"]
        recipient_id = request.form["recipient"]
        message = request.form["message"]
        status = send_message(token, recipient_id, message)
    return render_template("index.html", status=status)

app.run(host="0.0.0.0", port=81)
