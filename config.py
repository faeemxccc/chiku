import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("API_URL", "https://api.example.com/cricket") # Placeholder
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

EMOJI_GUIDE = {
    "live": "🔴",
    "upcoming": "⏳",
    "ended": "🏁",
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
    "Mujhe stress mat do, main already free tier pe hoon 😩",
    "Server itna free hai ki khud bhi kaam nahi karta 💀",
    "Amazon AWS nahi, Ammi Approved Server hoon main 😭",
    "High ping, low self-esteem 😔",
    "Running on hopes, dreams, and free credits 🥲",
    "Main bot hoon, bhagwan nahi 😌",
    "Aukat se zyada kaam = server down 💥",
    "Beta version hoon, stable nahi 🤡",
    "Mera server bhi Sunday manata hai 😴",
    "Garib server hu bhai, judge mat karo 😭"
]

PING_RESPONSES = [
    "😴 Uth gaya bhai… ",
    "☕ Arre haan haan, zinda hu… chai peeke aaya",
    "💀 Free server hoon, NASA ka computer nahi",
    "⚡ Ping mila, current aa gaya",
    "😮‍💨 Arre bhai shant… abhi hi jaga hoon",
    "🛌 Sone hi wala tha, tumne ping kar diya 😭",
    "🔋 1% battery pe jee raha hu, phir bhi online 😎",
    "👀 Haan haan dekh raha hu, ignore nahi kar raha",
    "🥲 Zinda hu… bas thoda broken",
    "🚶‍♂️ Server uth ke aaya… dheere dheere",
    "📶 Signal weak hai par niyat strong 😤",
    "🤖 Online ho gaya… emotional support nahi milega tho"
]
