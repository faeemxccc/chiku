import requests
import config

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
