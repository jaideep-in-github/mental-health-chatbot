# 🧠 AI Chatbot for Mental Health Support

An empathetic chatbot built to offer mental health support through natural, human-like conversations. It uses a pre-trained language model enhanced with emotional expressions and provides a clean web interface using Flask. This project explores the real-world application of AI in sensitive domains like emotional well-being.

---

## 💡 Overview

This chatbot listens, understands, and responds empathetically to user inputs with human-like qualities:

- 💬 **Natural Conversations** - Uses emotional expressions, follow-up questions, and varied phrasing
- 🌈 **Emotional Intelligence** - Recognizes and responds to different mental health topics
- 🛡️ **Crisis Detection** - Identifies potential crisis situations and provides appropriate resources
- 🧘 **Grounding Techniques** - Offers interactive exercises for anxiety management
- 📝 **Session Tracking** - Maintains conversation history for contextual responses

The model is based on Microsoft's DialoGPT and has been enhanced with rule-based responses to ensure supportive interactions even when the model is unavailable.

---

## 🧰 Tech Stack

- **Python 3.10+**
- **Transformers** (from Hugging Face)
- **Flask** (for web app and routing)
- **HTML + CSS** (for the frontend UI)
- **PyTorch** (for running the model)
- **DialoGPT** (Microsoft's conversational model)
- **Regular Expressions** (for filtering offensive content)

---

## 🚀 How It Works

1. User inputs a message through the chat interface on the webpage.
2. The input is processed through several layers:
   - **Offensive Language Filter** - Screens out inappropriate content
   - **Crisis Detection** - Identifies potential mental health emergencies
   - **Topic Detection** - Recognizes specific mental health topics (anxiety, depression, etc.)
   - **Response Generation** - Either uses the DialoGPT model or falls back to rule-based responses
   - **Emotional Enhancement** - Adds emotional expressions and follow-up questions
3. Both user input and bot reply are logged with timestamps and session IDs for context preservation.
4. The enhanced response is rendered back to the user with appropriate emotional cues.
5. The conversation continues with the chatbot maintaining context through session tracking.

---

## 🗂️ Project Structure

```
mental-health-chatbot/
├── app/
│   ├── chatbot.py      # Enhanced bot logic with emotional expressions
│   ├── logger.py       # Logs each user-bot exchange with session tracking
│   ├── routes.py       # Flask routes and core web logic
│   ├── static/
│   │   └── css/
│   │       └── style.css  # Responsive page styling
│   └── templates/
│       ├── index.html     # Main chat interface
│       ├── about.html     # About page with information
│       └── resources.html # Mental health resources page
├── logs/                  # Directory for session logs
│   └── session_*.json     # Individual session log files
├── run.py                 # App entry point
├── requirements.txt       # All dependencies
├── .gitignore             # Ignore venv, logs, pycache
└── sessions.log           # Master log file for all sessions
```

---

## 📷 Screenshots

![alt text](![image](https://github.com/user-attachments/assets/51d704f9-0895-45e8-be82-99c5b392e8d1)
)

---

## 📝 About This Project

- **Purpose**: This chatbot was created to explore how AI can provide emotional support in a responsible way.
- **Ethical Considerations**: The chatbot is designed with privacy and safety as priorities, with crisis detection and appropriate disclaimers.
- **Conversation Memory**: The model maintains a short-term memory of the conversation to provide contextually relevant responses.
- **Data Handling**: All conversations are stored with anonymous session IDs for improvement purposes only.
- **Limitations**: The chatbot doesn't give medical advice — it's designed solely for emotional support and to direct users to professional resources when needed.

---

## 🤝 Contributing

Contributions to improve the chatbot are welcome! Here are some ways you can help:

- **Enhanced Responses**: Add more empathetic responses for different mental health topics
- **UI Improvements**: Make the interface more accessible and user-friendly
- **Testing**: Help identify and fix issues or inappropriate responses
- **Documentation**: Improve this README or add more detailed documentation

To contribute:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🌟 Key Features

### Emotional Intelligence
- **Topic Detection** - Recognizes discussions about anxiety, depression, stress, loneliness, and grief
- **Empathetic Responses** - Provides supportive, understanding replies tailored to specific mental health topics
- **Human-like Conversation** - Uses emotional expressions, emojis, and natural language patterns

### Safety & Support
- **Crisis Detection** - Identifies potential crisis situations and provides helpline information
- **Offensive Language Filter** - Maintains a respectful conversation environment
- **Grounding Techniques** - Interactive exercises for anxiety management

### Technical Features
- **Fallback Mechanisms** - Functions even when the AI model cannot be loaded
- **Session Management** - Maintains conversation context across interactions
- **Responsive Design** - Works on both desktop and mobile devices

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+ installed
- Git (optional, for cloning)

### Step 1: Get the Code
```bash
# Clone the repository (or download ZIP)
git clone https://github.com/yourusername/mental-health-chatbot.git
cd mental-health-chatbot
```

### Step 2: Set Up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python run.py
```

### Step 5: Access the Chatbot
Open your browser and navigate to: http://127.0.0.1:5000

---

## 💡 Usage Tips

- **First-time Loading**: The first time you run the application, it may take a minute to download the DialoGPT model.
- **Conversation Topics**: Try discussing feelings of anxiety, stress, or sadness to see topic-specific responses.
- **Grounding Exercises**: Ask for help with anxiety to receive interactive grounding techniques.
- **Resources**: Check the Resources page for links to professional mental health services.
- **About Page**: Visit the About page to learn more about the chatbot's purpose and limitations.

---

## ⚠️ Limitations

- This chatbot is **NOT** a replacement for professional mental health care.
- It has limited understanding of complex mental health conditions.
- The AI model may occasionally generate inappropriate responses despite safeguards.
- All serious mental health concerns should be directed to qualified professionals.

---
