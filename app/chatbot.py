# Import necessary libraries
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
from typing import Dict, Optional, Tuple
import re
import random
import os

# Set environment variable to avoid warnings
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MentalHealthChatbot:
    def __init__(self, model_name: str = "microsoft/DialoGPT-small"):
        """Initialize the mental health chatbot with a specified model.
        
        Args:
            model_name: The pre-trained model to use (using smaller model for faster loading)
        """
        self.model_loaded = False
        self.sessions: Dict[str, torch.Tensor] = {}
        
        # Mental health specific responses
        self.crisis_keywords = ["suicide", "kill myself", "want to die", "end my life", "harm myself", "no reason to live"]
        self.crisis_response = "I'm really concerned about what you've shared. 💗 Your life matters deeply, and I want you to know that help is available right now. Please consider reaching out to the 988 Suicide & Crisis Lifeline (call or text 988) where caring professionals are waiting to talk with you. You don't have to face these feelings alone, and things can get better with support. Would it be okay if we focused on keeping you safe right now?"
        
        # Offensive language filter
        self.offensive_patterns = [
            r'\b(f+u+c+k+|s+h+i+t+|b+i+t+c+h+|d+i+c+k+|a+s+s+h+o+l+e+|c+u+n+t+)\b',
            r'\b(n+i+g+g+e+r+|f+a+g+g+o+t+)\b'
        ]
        self.offensive_response = "I notice the conversation has taken a turn. 🌱 I'm here to provide support in a respectful environment where we can both feel comfortable. I'd really like to understand what you're going through - perhaps we could try expressing that in different words? How can I best support your mental health needs today?"
        
        # Empathetic responses for common mental health concerns
        self.empathetic_responses = {
            "anxiety": [
                "I notice you're talking about anxiety. 🌬️ Taking slow, deep breaths can help in the moment. How are you feeling right now?",
                "Anxiety can be so challenging and overwhelming. Would it help to talk about what triggers these feelings for you?",
                "I understand anxiety can feel like a storm inside. Remember that you're stronger than you think. 💪 What's one thing that's helped you through anxious moments before?",
                "When my friends feel anxious, I remind them that these feelings will pass. You won't feel this way forever, I promise.",
                "It sounds like anxiety is really present for you right now. I'm here to listen and support you through this moment. 🌈"
            ],
            "depression": [
                "Depression can make everything feel so heavy. It's completely okay to take things one tiny step at a time. 🐢 What's one small thing you could do today?",
                "You're not alone in feeling this way, even though depression can make you feel isolated. Many people walk this path and find their way through the darkness.",
                "Even when it doesn't feel like it right now, there is always hope on the horizon. Would talking to a professional feel like a possibility for you?",
                "I hear how difficult things are feeling. Depression is like carrying a heavy backpack that no one else can see. I see you and your struggle. 💜",
                "On the hardest days, sometimes just getting out of bed is a victory. I'm proud of you for continuing to fight."
            ],
            "stress": [
                "I can hear the stress in what you're sharing. 🍃 Sometimes taking even a short 5-minute break can help reset your nervous system. Could you try that?",
                "Managing stress can be really difficult. What self-care activities have brought you moments of peace before?",
                "When I'm stressed, I try to focus on what's in my control and let go of what isn't. Maybe we could identify what parts of your situation you can influence?",
                "Stress can build up in our bodies without us even noticing. Are you holding tension somewhere right now? Maybe in your shoulders or jaw?",
                "It sounds like you're carrying a lot right now. Remember that asking for help isn't weakness - it's wisdom. 🦉"
            ],
            "loneliness": [
                "Feeling lonely is such a universal human experience, even though it makes us feel so separate from others. 🌎 Remember that connections can come in unexpected forms.",
                "It takes real courage to acknowledge feelings of loneliness. Have you thought about small ways to connect with others who share your interests?",
                "Even though loneliness feels so isolating, please know that many people understand exactly what you're going through. You're not alone in feeling alone.",
                "Sometimes loneliness visits us even when we're surrounded by people. It's about feeling truly seen and understood. Do you feel that way often?",
                "I'm really glad you're talking to me about this. Sharing these feelings is actually the first step toward connection. 🌱"
            ],
            "grief": [
                "Grief has no timeline or roadmap. Be gentle with yourself as you navigate these deep feelings. 🕊️ What do you miss most?",
                "It's completely okay to miss someone and feel that loss deeply. Your feelings are so valid, and your grief is a reflection of your love.",
                "Healing from loss happens gradually, in waves that come and go. Allow yourself to feel without judgment. I'm here with you in this moment.",
                "Sometimes grief can feel like carrying someone in your heart while learning to live without them in your life. That's an enormous challenge.",
                "On difficult days, it can help to honor your loved one in small ways. Is there a memory or tradition that brings you comfort?"
            ]
        }
            
        # Grounding techniques for anxiety or panic
        self.grounding_techniques = [
            "I can sense you might need something to help ground you right now. 🌿 Let's try the 5-4-3-2-1 technique together: Can you tell me 5 things you see around you right now?",
            "When I feel overwhelmed, this helps me: Place your feet firmly on the ground and really notice the sensation of the floor supporting you. Feel that connection to the earth. How does that feel?",
            "Let's take a moment together. 🧘 Can you try taking 10 slow, deep breaths with me? Breathe in... and out... focusing completely on the feeling of your breath. I'm right here with you.",
            "Something that might help right now: If you can, try running cool or warm water over your hands and focus on how it feels against your skin. The temperature, the sensation. It can really bring you back to the present moment.",
            "Let's try a simple exercise that helps many people: Can you name 5 colors you can see around you right now? Just noticing these details can help your mind refocus and calm down a bit. 💙",
            "I wonder if we could try something together? Place one hand on your heart and one on your stomach. Feel your chest rise and fall as you breathe. This connection to your body can be really grounding when anxiety feels overwhelming."
        ]
        
        # General supportive responses when model is not available
        self.supportive_responses = [
            "I'm here to listen. How can I support you today? 💙",
            "It takes courage to share your feelings. Thank you for trusting me with them. 🌱",
            "Remember that it's okay to not be okay sometimes. What's on your mind right now?",
            "I'm here to support you. Would you like to talk more about what you're experiencing? I'm all ears.",
            "Your feelings are valid and important. What would be most helpful for you right now?",
            "Sometimes just having someone to talk to can make a difference. I'm here for you. ✨",
            "I'm really glad you reached out today. How are you feeling in this moment?",
            "Taking care of your mental health is so important. I'm proud of you for doing that today. 💪",
            "I'm sensing this might be difficult to talk about. Take your time, there's no rush.",
            "Everyone struggles sometimes - you're not alone in this. How can I help lighten your load today?"
        ]
        
        # Conversation starters and follow-up questions
        self.follow_up_questions = [
            "How long have you been feeling this way?",
            "What helps you feel better when you're going through tough times?",
            "Have you talked to anyone else about this?",
            "On a scale of 1-10, how would you rate how you're feeling today?",
            "What's one small thing that brought you joy recently?",
            "Is there something specific that triggered these feelings?",
            "What would a good day look like for you right now?",
            "Have you tried any coping strategies that have worked before?"
        ]
        
        # Emotional expressions to make responses more human-like
        self.emotional_expressions = {
            "empathy": ["I understand how difficult that must be", "That sounds really challenging", "I can imagine how that feels"],
            "encouragement": ["You're doing great by reaching out", "Every small step matters", "I believe in your ability to get through this"],
            "validation": ["Your feelings are completely valid", "It makes sense that you feel that way", "Anyone would struggle with that"],
            "warmth": ["I'm here with you", "You're not alone in this journey", "I'm sending you good thoughts"]
        }
        
        # Try to load the model, but continue even if it fails
        try:
            logger.info(f"Loading model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            self.model_loaded = True
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            logger.info("Continuing with rule-based responses only")

    def detect_mental_health_topic(self, text: str) -> Optional[str]:
        """Detect mental health topics in user input.
        
        Args:
            text: The user's message
            
        Returns:
            The detected topic if found, None otherwise
        """
        text = text.lower()
        if any(word in text for word in ["anxious", "anxiety", "nervous", "worry", "panic"]):
            return "anxiety"
        elif any(word in text for word in ["depress", "sad", "hopeless", "unmotivated", "empty"]):
            return "depression"
        elif any(word in text for word in ["stress", "overwhelm", "pressure", "burnout"]):
            return "stress"
        elif any(word in text for word in ["alone", "lonely", "no friends", "isolated", "no one"]):
            return "loneliness"
        elif any(word in text for word in ["grief", "loss", "died", "passed away", "missing someone"]):
            return "grief"
        return None

    def is_offensive(self, text: str) -> bool:
        """Check if the input contains offensive language.
        
        Args:
            text: The input text to check
            
        Returns:
            True if offensive language is detected, False otherwise
        """
        for pattern in self.offensive_patterns:
            if re.search(pattern, text.lower()):
                return True
        return False

    def get_response(self, user_input: str, session_id: str = "default") -> str:
        """Generate a response to the user input.
        
        Args:
            user_input: The user's message
            session_id: Unique identifier for the conversation session
            
        Returns:
            The chatbot's response
        """
        try:
            # Check for offensive language
            if self.is_offensive(user_input):
                return self.offensive_response
                
            # Check for crisis keywords
            if any(keyword in user_input.lower() for keyword in self.crisis_keywords):
                return self.crisis_response
            
            # Helper function to add emotional expressions
            def add_emotion(response, emotion_type=None):
                if emotion_type is None:
                    # Randomly select an emotion type
                    emotion_type = random.choice(list(self.emotional_expressions.keys()))
                
                # 60% chance to add an emotional expression
                if random.random() < 0.6:
                    emotion = random.choice(self.emotional_expressions[emotion_type])
                    return f"{emotion}. {response}"
                return response
            
            # Helper function to add follow-up questions
            def add_follow_up(response):
                # 50% chance to add a follow-up question
                if random.random() < 0.5 and not response.endswith("?"):
                    follow_up = random.choice(self.follow_up_questions)
                    return f"{response} {follow_up}"
                return response
                
            # Check for mental health topics
            topic = self.detect_mental_health_topic(user_input)
            if topic and random.random() < 0.8:  # Increased chance to use empathetic responses
                response = random.choice(self.empathetic_responses[topic])
                return response  # These already have emotional content and follow-ups
                
            # Special case for anxiety with grounding techniques
            if topic == "anxiety" and ("help" in user_input.lower() or "anxious" in user_input.lower()) and random.random() < 0.6:
                return random.choice(self.grounding_techniques)
            
            # If model is not loaded, use rule-based responses
            if not self.model_loaded:
                response = random.choice(self.supportive_responses)
                # These already have emotional content, but we might add a follow-up
                if not "?" in response:
                    return add_follow_up(response)
                return response
            
            # Model-based response generation (only if model is loaded)
            # Encode user input
            new_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, 
                                               return_tensors='pt')
            
            # Get or create chat history
            chat_history_ids = self.sessions.get(session_id)
            
            if chat_history_ids is not None:
                bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
            else:
                bot_input_ids = new_input_ids
            
            # Generate response with better parameters for mental health conversations
            chat_history_ids = self.model.generate(
                bot_input_ids,
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id,
                no_repeat_ngram_size=3,
                do_sample=True,
                temperature=0.7,
                top_p=0.92,
                top_k=50
            )
            
            # Save the chat history
            self.sessions[session_id] = chat_history_ids
            
            # Decode and return
            response = self.tokenizer.decode(
                chat_history_ids[:, bot_input_ids.shape[-1]:][0], 
                skip_special_tokens=True
            )
            
            # If empty or too short, give a supportive response
            if not response.strip() or len(response.split()) < 3:
                short_responses = [
                    "I'm here to listen and support you. Could you share more about what you're experiencing? 💭",
                    "I'd really like to understand better. Can you tell me a bit more about what's on your mind?",
                    "Sometimes it helps to put feelings into words. Would you like to try explaining a bit more?",
                    "I want to be here for you in the best way possible. Could you share a little more detail?"
                ]
                return random.choice(short_responses)
            
            # Enhance model response with emotional expressions and follow-ups
            # 40% chance to enhance model response
            if random.random() < 0.4:
                # Add emotional expression
                if random.random() < 0.5:
                    emotion_type = random.choice(list(self.emotional_expressions.keys()))
                    emotion = random.choice(self.emotional_expressions[emotion_type])
                    response = f"{emotion}. {response}"
                
                # Add follow-up question if response doesn't already end with one
                if not response.strip().endswith("?") and random.random() < 0.4:
                    follow_up = random.choice(self.follow_up_questions)
                    response = f"{response} {follow_up}"
            
            # 20% chance to add an emoji to make it more human-like
            if random.random() < 0.2:
                emojis = ["💭", "💙", "🌱", "✨", "🌈", "🧡", "🤔", "💪", "🌿"]
                response = f"{response} {random.choice(emojis)}"
                
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Fall back to rule-based responses on error
            return random.choice(self.supportive_responses)
    
    def reset_chat(self, session_id: str = "default") -> None:
        """Reset the chat history for a given session.
        
        Args:
            session_id: The session ID to reset
        """
        if self.model_loaded and session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Reset chat session: {session_id}")
        else:
            logger.info(f"No session to reset or model not loaded: {session_id}")

# Initialize a default chatbot instance
default_chatbot = MentalHealthChatbot()

def get_bot_response(user_input: str, session_id: str = "default") -> str:
    """Get a response from the chatbot for the given user input.
    
    Args:
        user_input: The user's message
        session_id: Unique identifier for the conversation session
        
    Returns:
        The chatbot's response
    """
    return default_chatbot.get_response(user_input, session_id)
