import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL", "https://api.example.com/cricket") # Placeholder

EMOJI_GUIDE = {
    "live": "🔴",
    "upcoming": "⏳",
    "cricket": "🏏",
    "status": "📢",
    "team": "🟦🟥🟢🟡",
    "warning": "⚠️"
}

JOKES_POOL = [
    "Free server hu bhai, 24/7 majdoor nahi 😭",
    "Server: 1GB RAM. Sapne: 64GB 😔",
    "Itna load mat daal, meri aukaat limited hai 💀",
    "Cloud pe hoon, par sasta wala cloud ☁️😂",
    "Production bot nahi hoon, jugaad edition hoon 😎",
    "Bot hoon, bhagwan nahi 😌"
]

PING_RESPONSES = [
    "😴 Uth gaya bhai… free server main kaam kar raha hu",
    "☕ Arre haan haan, zinda hu… chai peeke aaya",
    "💀 Free server hoon, NASA ka computer nahi",
    "⚡ Ping mila, current aa gaya"
]
