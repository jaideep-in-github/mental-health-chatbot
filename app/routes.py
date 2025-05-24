from flask import Flask, render_template, request
from app.chatbot import get_bot_response
from app.logger import log_session

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    bot_reply = ""
    if request.method == "POST":
        user_input = request.form["message"]
        bot_reply = get_bot_response(user_input)
        log_session(user_input, bot_reply)
    return render_template("index.html", bot_reply=bot_reply)
