# run.py
from app.routes import app

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)  # Disable auto-reload
