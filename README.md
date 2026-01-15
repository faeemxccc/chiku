# SleepyCricketBot 😴🏏

A sarcastic, desi discord bot that fetches live cricket scores and displays them with a sleepy attitude.

## Features
- **Live Scores**: Fetches real-time cricket scores.
- **Sarcastic Persona**: Responds with sleepy, funny Hinglish dialogues.
- **Slash Commands**: Supports `/score`, `/live`, `/upcoming`, and `/ping`.
- **Smart Grouping**: Groups matches into Live and Upcoming categories to reduce spam.
- **Resilient**: Handles API timeouts gracefully.

## Setup

1.  **Clone the repo**
    ```bash
    git clone https://github.com/yourusername/SleepyCricketBot.git
    cd SleepyCricketBot
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\Activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Create a `.env` file in the root directory:
    ```env
    DISCORD_TOKEN=your_discord_bot_token_here
    API_URL=https://py-score-api.onrender.com/live-matches
    ```

5.  **Run the Bot**
    ```bash
    python bot.py
    ```

## Commands
- `/ping` - Check if bot is awake.
- `/score` - Show all matches.
- `/live` - Show only live matches.
- `/upcoming` - Show upcoming matches.
- `!sync` - Sync commands with Discord (Admin only).

## License
MIT
