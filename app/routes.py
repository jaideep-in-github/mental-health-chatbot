from flask import Flask, request, jsonify, render_template, session
import uuid
from datetime import datetime
import os
from app.chatbot import get_bot_response, default_chatbot
from app.logger import log_conversation

# Initialize app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

@app.route('/')
def home():
    """Render the home page."""
    # Generate a session ID if one doesn't exist
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint to get a response from the chatbot."""
    data = request.json
    user_message = data.get('message', '')
    
    # Get or create session ID
    session_id = session.get('session_id', str(uuid.uuid4()))
    if 'session_id' not in session:
        session['session_id'] = session_id
    
    # Get response from chatbot
    bot_response = get_bot_response(user_message, session_id)
    
    # Log the conversation
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_conversation(session_id, timestamp, user_message, bot_response)
    
    return jsonify({
        'response': bot_response,
        'session_id': session_id
    })

@app.route('/api/reset', methods=['POST'])
def reset_chat():
    """API endpoint to reset the chat session."""
    session_id = session.get('session_id')
    if session_id:
        default_chatbot.reset_chat(session_id)
        
    # Create a new session ID
    session['session_id'] = str(uuid.uuid4())
    
    return jsonify({
        'status': 'success',
        'message': 'Chat session reset successfully',
        'session_id': session['session_id']
    })

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')

@app.route('/resources')
def resources():
    """Render the mental health resources page."""
    return render_template('resources.html')

if __name__ == '__main__':
    app.run(debug=True)
