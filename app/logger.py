from datetime import datetime

def log_session(user_input, bot_response):
    with open("sessions.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | User: {user_input} | Bot: {bot_response}\n")
