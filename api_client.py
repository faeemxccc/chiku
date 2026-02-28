import requests
import config
import json
import os
import time
def fetch_matches():
    """
    Fetches matches from the configured API endpoint.
    Returns a list of match dictionaries.
    """
    try:
        response = requests.get(config.API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Ensure data is a list; adjust based on actual API response structure
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "matches" in data:
            return data["matches"]
        else:
            print(f"⚠️ Unexpected API response format: {data}")
            return []
            
    except requests.exceptions.Timeout:
        print("⚠️ API Request Timed Out")
        return None # Explicit timeout signal
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API Request Failed: {e}")
        return None # Explicit failure signal

def get_live_matches():
    matches = fetch_matches()
    if matches is None: return None
    return [m for m in matches if m.get("is_live") is True]

def get_upcoming_matches():
    matches = fetch_matches()
    if matches is None: return None
    # Upcoming = Not live AND No scores yet
    return [m for m in matches if m.get("is_live") is False and not m.get("scores")]

def get_ended_matches():
    matches = fetch_matches()
    if matches is None: return None
    # Ended = Not live AND Has scores
    return [m for m in matches if m.get("is_live") is False and m.get("scores")]

def fetch_meme():
    """
    Fetches a random meme from the meme-api.com
    """
    try:
        response = requests.get("https://meme-api.com/gimme", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Meme API Request Failed: {e}")
        return None

# --- AI Chat via Direct Endpoint ---

def _load_context():
    """Loads the entire context from the JSON file."""
    if not os.path.exists(config.CONTEXT_FILE):
        return {}
    try:
        with open(config.CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading context file: {e}")
        return {}

def _save_context(context_data):
    """Saves the entire context to the JSON file."""
    try:
        with open(config.CONTEXT_FILE, "w", encoding="utf-8") as f:
            json.dump(context_data, f, indent=4)
    except Exception as e:
        print(f"⚠️ Error saving context file: {e}")

def get_ai_response(channel_id, user_name, user_message):
    """
    Calls the Gemini API endpoint directly, maintaining conversation history per channel in a JSON file.
    Includes the user's name to personalize the conversation.
    """
    if not config.GOOGLE_API_KEY:
        return "⚠️ I can't think right now, Google API Key is missing."

    channel_id_str = str(channel_id)
    all_contexts = _load_context()
    
    # Get history for this channel (default to empty list if none)
    channel_history = all_contexts.get(channel_id_str, [])

    # Format the current message to include the user's name for personalization
    formatted_message = f"[User: {user_name}] {user_message}"

    # Build the 'contents' array as required by the Gemini REST API
    contents = []
    
    # System instructions and guidelines can be passed as the first message or as a system Instruction. 
    # For Gemini 1.5/flash standard REST endpoint, we can use the 'systemInstruction' field, 
    # or just prepend a context setting message.
    # To be safe across versions, let's prepend an initial context if the history is empty or rely on systemInstruction if we use it.
    
    # We will use systemInstruction in the payload as it's the recommended way.
    system_instruction = {
        "role": "model",
        "parts": [{"text": "You are a helpful and personal discord bot. Users will send messages starting with [User: Name] so you know who is talking. Always respond concisely and try to refer to the user by their name to make it personal. Focus on conversational chat. Remember the context of the conversation in this channel."}]
    }

    current_time = time.time()
    
    # 1. Check user activity: user messages in the last 60 minutes
    # We check if there are previous user messages from this user within the last hour
    user_prefix = f"[User: {user_name}]"
    recent_user_msgs = [
        msg for msg in channel_history 
        if msg.get("role") == "user" 
           and msg.get("text", "").startswith(user_prefix)
           and msg.get("timestamp", 0) >= (current_time - 3600)
    ]
    
    is_active = len(recent_user_msgs) > 0

    if not is_active:
        history_limit = 3
    else:
        # 2. Check for large messages in recent history
        recent_10 = channel_history[-10:]
        has_large_msg = any(len(msg.get("text", "")) > 500 for msg in recent_10)
        
        if has_large_msg:
            history_limit = 5
        else:
            history_limit = 10
            
    # Restrict the history we send to the AI (leaving room for the current message)
    history_to_send = channel_history[-(history_limit-1):] if history_limit > 1 else []

    # Add historical messages
    for msg in history_to_send:
        role = "user" if msg.get("role", "user") == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg.get("text", "")}]
        })

    # Add the current message
    contents.append({
        "role": "user",
        "parts": [{"text": formatted_message}]
    })

    # Direct Gemini API URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={config.GOOGLE_API_KEY}"
    
    payload = {
        "contents": contents,
        "systemInstruction": system_instruction
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Parse the AI response from the structure
        try:
            ai_text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            print(f"⚠️ Unexpected AI API response Format: {data}")
            return "⚠️ I got confused trying to read my own thoughts."

        # Append new messages to history
        current_time_post = time.time()
        channel_history.append({"role": "user", "text": formatted_message, "timestamp": current_time_post})
        channel_history.append({"role": "model", "text": ai_text, "timestamp": current_time_post})

        # Save back the updated history
        all_contexts[channel_id_str] = channel_history
        _save_context(all_contexts)

        return ai_text

    except requests.exceptions.Timeout:
        return "🐢 Mmmm my brain is a bit slow right now, request timed out."
    except requests.exceptions.RequestException as e:
        print(f"⚠️ AI API Request Failed: {e}")
        # Could be an HTTPError with details
        if hasattr(e, 'response') and e.response is not None:
             print(f"Response: {e.response.text}")
        return f"⚠️ Thinking process crashed: {e}"

