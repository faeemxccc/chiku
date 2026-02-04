import requests
import config
from google import genai
from google.genai.types import HttpOptions
import json
import google.genai.types as types
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
def generate_content(user_prompt):
    # 1. Initialize the client
    # Ensure your GOOGLE_API_KEY environment variable is set!
    client = genai.Client(api_key=config.GOOGLE_API_KEY)

    system_instruction = (
        "You are Chikku, a friendly and slightly funny Discord bot. "
        "Keep responses brief and polite, add a light humorous touch when appropriate. "
        "Format answers in Markdown suitable for Discord."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=100,
            ),
        )
        
        # In the new SDK, .text is the standard way to get the string
        return response.text

    except Exception as e:
        # Combined error handling: print to console for you, return message for Discord
        print(f"⚠️ GenAI request failed: {e}")
        return f"Oops! Chikku hit a snag: {e}"