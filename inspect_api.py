import requests
import json

API_URL = "https://py-score-api.onrender.com/live-matches"

try:
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    data = response.json()
    print(json.dumps(data, indent=2))
except Exception as e:
    print(f"Error: {e}")
