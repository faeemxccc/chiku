# SleepyCricketBot 😴🏏

A sarcastic, desi discord bot that fetches live cricket scores and displays them with a sleepy attitude.

## Features
- **Live Scores**: Fetches real-time cricket scores.
- **Sarcastic Persona**: Responds with sleepy, funny Hinglish dialogues.
- **AI Chat integration**: Responds using the Gemini API directly, maintaining the context of each channel with tailored, personalized replies.
- **Dynamic Context Sizing**: Smartly curates the AI conversation history based on user activity (within the last hour) and message constraints (size > 500 characters) to optimize token usage.
- **Memories Dashboard**: A local Flask web dashboard to view, edit, and delete conversation histories interactively.
- **Slash Commands**: Supports `/score`, `/live`, `/upcoming`, `/meme`, and `/ping`.
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
    pip install flask requests discord.py
    ```

4.  **Configuration**
    Create a `.env` file in the root directory:
    ```env
    DISCORD_TOKEN=your_discord_bot_token_here
    GOOGLE_API_KEY=your_gemini_api_key_here
    API_URL=https://py-score-api.onrender.com/live-matches
    ```

5.  **Run the Bot & Dashboard**
    Start the Discord Bot:
    ```bash
    python bot.py
    ```
    
    In a separate terminal, start the Memories Dashboard to manage AI conversation history:
    ```bash
    python dashboard.py
    ```
    Access the dashboard at `http://127.0.0.1:5000`.

## Commands
- `/ping` - Check if bot is awake.
- `/score` - Show all matches.
- `/live` - Show only live matches.
- `/upcoming` - Show upcoming matches.
- `!sync` - Sync commands with Discord (Admin only).

## License
MIT
