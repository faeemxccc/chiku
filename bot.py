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
    upcoming_matches = [m for m in matches if not m.get("is_live")]

    if live_matches:
        embed = utils.create_grouped_match_embed(live_matches, "🔴 Live Matches", 0xFF0000)
        await ctx.send(embed=embed)
    
    if upcoming_matches:
        embed = utils.create_grouped_match_embed(upcoming_matches, "⏳ Upcoming Matches", 0x3498DB)
        await ctx.send(embed=embed)

@bot.command(name='live', help='Shows only live matches')
async def live(ctx):
    matches = api_client.get_live_matches()
    if not matches:
        await ctx.send(config.EMOJI_GUIDE["warning"] + " " + "🔕 Aaj shanti hai… koi match live nahi hai bhai")
        return

    for match in matches:
        embed = utils.create_match_embed(match)
        await ctx.send(embed=embed)

@bot.command(name='upcoming', help='Shows only upcoming matches')
async def upcoming(ctx):
    matches = api_client.get_upcoming_matches()
    if not matches:
        await ctx.send("😴 Sab so rahe hain... koi upcoming match nahi mila.")
        return

    for match in matches:
        embed = utils.create_match_embed(match)
        await ctx.send(embed=embed)

@bot.command(name='allmatches', help='Lists all matches with live/upcoming tag')
async def allmatches(ctx):
    matches = api_client.fetch_matches()
    if not matches:
        await ctx.send(random.choice(config.JOKES_POOL))
        return

    response_lines = []
    for match in matches:
        tag = "🔴 LIVE" if match.get("is_live") else "⏳ UPCOMING"
        name = match.get("name", "Unknown Match")
        response_lines.append(f"{tag} {name}")
    
    await ctx.send("\n".join(response_lines))

@bot.command(name='help_me', help='Shows all available commands')
async def help_command(ctx):
     await ctx.send("📜 Thoda padh bhi liya kar 😅 ye le commands list\n"
                    "**!ping** - Check if I'm alive\n"
                    "**!score** - All matches cards\n"
                    "**!live** - Live matches only\n"
                    "**!upcoming** - Upcoming matches only\n"
                    "**!allmatches** - List all match titles (compact)\n"
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

@bot.tree.command(name="score", description="Fetches and displays all live/upcoming matches")
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
    upcoming_matches = [m for m in matches if not m.get("is_live")]

    if live_matches:
        embed = utils.create_grouped_match_embed(live_matches, "🔴 Live Matches", 0xFF0000)
        await interaction.followup.send(embed=embed)
    
    if upcoming_matches:
        embed = utils.create_grouped_match_embed(upcoming_matches, "⏳ Upcoming Matches", 0x3498DB)
        await interaction.followup.send(embed=embed)
    
    if not live_matches and not upcoming_matches:
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


if __name__ == "__main__":
    if config.DISCORD_TOKEN:
        bot.run(config.DISCORD_TOKEN)
    else:
        print("⚠️ DISCORD_TOKEN not found. Please set it in .env or config.py")
