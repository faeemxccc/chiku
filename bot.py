import discord
from discord.ext import commands
import config
import random
import asyncio
import api_client
import utils

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'😴 {bot.user.name} is awake... barely.')

@bot.command(name='ping', help='Wakes up the free server and confirms the bot is alive')
async def ping(ctx):
    response = random.choice(config.PING_RESPONSES)
    await ctx.send(response)

@bot.command(name='score', help='Fetches and displays all matches with emojis')
async def score(ctx):
    matches = api_client.fetch_matches()
    if not matches:
        await ctx.send(config.EMOJI_GUIDE["warning"] + " " + random.choice(config.JOKES_POOL))
        return

    live_matches = [m for m in matches if m.get("is_live")]
    # Upcoming: Not live AND No scores
    upcoming_matches = [m for m in matches if not m.get("is_live") and not m.get("scores")]
    # Ended: Not live AND Has scores
    ended_matches = [m for m in matches if not m.get("is_live") and m.get("scores")]

    if live_matches:
        embed = utils.create_grouped_match_embed(live_matches, "🔴 Live Matches", 0xFF0000)
        await ctx.send(embed=embed)
    
    if upcoming_matches:
        embed = utils.create_grouped_match_embed(upcoming_matches, "⏳ Upcoming Matches", 0x3498DB)
        await ctx.send(embed=embed)
        
    if ended_matches:
        embed = utils.create_grouped_match_embed(ended_matches, "🏁 Ended Matches", 0x95A5A6)
        await ctx.send(embed=embed)

@bot.command(name='live', help='Shows only live matches')
async def live(ctx):
    matches = api_client.get_live_matches()
    if not matches:
        await ctx.send(config.EMOJI_GUIDE["warning"] + " " + "🔕 Aaj shanti hai… koi match live nahi hai bhai")
        return

    for match in matches:
        embed = utils.create_match_embed(match, category="live")
        await ctx.send(embed=embed)

@bot.command(name='upcoming', help='Shows only upcoming matches')
async def upcoming(ctx):
    matches = api_client.get_upcoming_matches()
    if not matches:
        await ctx.send("😴 Sab so rahe hain... koi upcoming match nahi mila.")
        return

    for match in matches:
        embed = utils.create_match_embed(match, category="upcoming")
        await ctx.send(embed=embed)

@bot.command(name='ended', help='Shows only ended matches')
async def ended(ctx):
    matches = api_client.get_ended_matches()
    if not matches:
        await ctx.send("Khatam tata bye bye... koi ended match nahi hai.")
        return

    for match in matches:
        embed = utils.create_match_embed(match, category="ended")
        await ctx.send(embed=embed)

@bot.command(name='allmatches', help='Lists all matches with live/upcoming/ended tag')
async def allmatches(ctx):
    matches = api_client.fetch_matches()
    if not matches:
        await ctx.send(random.choice(config.JOKES_POOL))
        return

    response_lines = []
    for match in matches:
        if match.get("is_live"):
            tag = "🔴 LIVE"
        elif match.get("scores"):
            tag = "🏁 ENDED"
        else:
            tag = "⏳ UPCOMING"
            
        name = match.get("name", "Unknown Match")
        # Fallback if name is missing but match key exists
        if name == "Unknown Match" and match.get("match"):
            name = match.get("match")
            
        response_lines.append(f"{tag} {name}")
    
    await ctx.send("\n".join(response_lines))

@bot.command(name='help_me', help='Shows all available commands')
async def help_command(ctx):
     await ctx.send("📜 Thoda padh bhi liya kar 😅 ye le commands list\n"
                    "**!ping** - Check if I'm alive\n"
                    "**!score** - All matches cards (Live, Upcoming, Ended)\n"
                    "**!live** - Live matches only\n"
                    "**!upcoming** - Upcoming matches only\n"
                    "**!ended** - Ended matches only\n"
                    "**!allmatches** - List all match titles (compact)\n"
                    "**!meme** - Get a random meme 🤣\n"
                    "**!sync** - Sync slash commands (Admin only)\n"
                    "**!help_me** - This message")

# --- Slash Commands ---

@bot.command()
async def sync(ctx):
    """Syncs slash commands with Discord"""
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"Synced {len(synced)} slash commands! ⚡")
    except Exception as e:
        await ctx.send(f"Failed to sync: {e}")

@bot.tree.command(name="ping", description="Wakes up the free server and confirms the bot is alive")
async def slash_ping(interaction: discord.Interaction):
    response = random.choice(config.PING_RESPONSES)
    await interaction.response.send_message(response)

@bot.tree.command(name="score", description="Fetches and displays all matches")
async def slash_score(interaction: discord.Interaction):
    await interaction.response.defer() # Defer because API call might be slow
    matches = api_client.fetch_matches()
    
    if matches is None:
        await interaction.followup.send("🐢 **Server slow hai bhai...** API is waking up. Try again in 30 seconds.")
        return

    if not matches:
        await interaction.followup.send(config.EMOJI_GUIDE["warning"] + " " + random.choice(config.JOKES_POOL))
        return

    live_matches = [m for m in matches if m.get("is_live")]
    upcoming_matches = [m for m in matches if not m.get("is_live") and not m.get("scores")]
    ended_matches = [m for m in matches if not m.get("is_live") and m.get("scores")]

    has_content = False

    if live_matches:
        embed = utils.create_grouped_match_embed(live_matches, "🔴 Live Matches", 0xFF0000)
        await interaction.followup.send(embed=embed)
        has_content = True
    
    if upcoming_matches:
        embed = utils.create_grouped_match_embed(upcoming_matches, "⏳ Upcoming Matches", 0x3498DB)
        await interaction.followup.send(embed=embed)
        has_content = True
        
    if ended_matches:
        embed = utils.create_grouped_match_embed(ended_matches, "🏁 Ended Matches", 0x95A5A6)
        await interaction.followup.send(embed=embed)
        has_content = True
    
    if not has_content:
         await interaction.followup.send("No matches found at all. Go sleep.")

@bot.tree.command(name="live", description="Shows only live matches")
async def slash_live(interaction: discord.Interaction):
    await interaction.response.defer()
    matches = api_client.get_live_matches()

    if matches is None:
        await interaction.followup.send("🐢 **Server slow hai bhai...** API is waking up. Try again in 30 seconds.")
        return

    if not matches:
        await interaction.followup.send(config.EMOJI_GUIDE["warning"] + " " + "🔕 Aaj shanti hai… koi match live nahi hai bhai")
        return

    embed = utils.create_grouped_match_embed(matches, "🔴 Live Matches", 0xFF0000)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="upcoming", description="Shows only upcoming matches")
async def slash_upcoming(interaction: discord.Interaction):
    await interaction.response.defer()
    matches = api_client.get_upcoming_matches()

    if matches is None:
        await interaction.followup.send("🐢 **Server slow hai bhai...** API is waking up. Try again in 30 seconds.")
        return

    if not matches:
        await interaction.followup.send("😴 Sab so rahe hain... koi upcoming match nahi mila.")
        return

    embed = utils.create_grouped_match_embed(matches, "⏳ Upcoming Matches", 0x3498DB)
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="ended", description="Shows only ended matches")
async def slash_ended(interaction: discord.Interaction):
    await interaction.response.defer()
    matches = api_client.get_ended_matches()

    if matches is None:
        await interaction.followup.send("🐢 **Server slow hai bhai...** API is waking up. Try again in 30 seconds.")
        return

    if not matches:
        await interaction.followup.send("Khatam tata bye bye... koi ended match nahi hai.")
        return

    embed = utils.create_grouped_match_embed(matches, "🏁 Ended Matches", 0x95A5A6)
    await interaction.followup.send(embed=embed)

@bot.command(name='meme', help='Get a random meme')
async def meme(ctx):
    meme_data = api_client.fetch_meme()
    if not meme_data:
        await ctx.send("Could not fetch a meme. 😢")
        return
    embed = utils.create_meme_embed(meme_data)
    await ctx.send(embed=embed)

@bot.tree.command(name="meme", description="Get a random meme")
async def slash_meme(interaction: discord.Interaction):
    await interaction.response.defer()
    meme_data = api_client.fetch_meme()
    if not meme_data:
        await interaction.followup.send("Could not fetch a meme. 😢")
        return
    embed = utils.create_meme_embed(meme_data)
    await interaction.followup.send(embed=embed)

if __name__ == "__main__":
    if config.DISCORD_TOKEN:
        bot.run(config.DISCORD_TOKEN)
    else:
        print("⚠️ DISCORD_TOKEN not found. Please set it in .env or config.py")
