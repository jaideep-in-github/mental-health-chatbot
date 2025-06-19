import logging
import os
from typing import Dict, Any
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename="sessions.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

def log_conversation(session_id: str, timestamp: str, user_message: str, bot_response: str) -> None:
    """Log a conversation between user and bot.
    
    Args:
        session_id: Unique session identifier
        timestamp: Time of the message
        user_message: Message from the user
        bot_response: Response from the chatbot
    """
    # Log to console
    print(f"[{timestamp}] Session {session_id}: User: {user_message} | Bot: {bot_response}")
    
    # Log to file
    log_entry = {
        "session_id": session_id,
        "timestamp": timestamp,
        "user_message": user_message,
        "bot_response": bot_response
    }
    
    # Append to main log file
    logging.info(f"Session: {session_id} | User: {user_message} | Bot: {bot_response}")
    
    # Save session-specific logs
    session_file = f"logs/session_{session_id}.json"
    
    try:
        # Load existing log if it exists
        if os.path.exists(session_file):
            with open(session_file, "r") as f:
                try:
                    session_logs = json.load(f)
                except json.JSONDecodeError:
                    session_logs = {"session_id": session_id, "conversations": []}
        else:
            session_logs = {"session_id": session_id, "conversations": []}
        
        # Add new entry
        session_logs["conversations"].append({
            "timestamp": timestamp,
            "user_message": user_message,
            "bot_response": bot_response
        })
        
        # Write back to file
        with open(session_file, "w") as f:
            json.dump(session_logs, f, indent=2)
    
    except Exception as e:
        logging.error(f"Error writing to session log: {e}")

def get_session_history(session_id: str) -> Dict[str, Any]:
    """Retrieve conversation history for a specific session.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        Dictionary containing the session conversation history
    """
    session_file = f"logs/session_{session_id}.json"
    
    if os.path.exists(session_file):
        try:
            with open(session_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error reading session log: {e}")
            return {"session_id": session_id, "conversations": []}
    else:
        return {"session_id": session_id, "conversations": []}
