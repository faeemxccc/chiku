import discord
import config

def create_match_embed(match, category="general"):
    """
    Creates a Discord Embed for a single match.
    Category can be: 'live', 'upcoming', 'ended', 'general'
    """
    scores_list = match.get("scores", [])
    if len(scores_list) >= 2:
        team1 = scores_list[0].get("team", "Team 1")
        score1 = scores_list[0].get("score", "-")
        team2 = scores_list[1].get("team", "Team 2")
        score2 = scores_list[1].get("score", "-")
    elif len(scores_list) == 1:
        team1 = scores_list[0].get("team", "Team 1")
        score1 = scores_list[0].get("score", "-")
        team2 = "TBA"
        score2 = "-"
    else:
        team1 = "Team 1"
        score1 = "-"
        team2 = "Team 2"
        score2 = "-"

    match_name = match.get("match", "N/A")
    if match_name == "N/A" or not match_name:
        match_name = f"{team1} vs {team2}"
    
    status = match.get("status", "No status")
    is_live = match.get("is_live", False)
    
    # Determine Color & Prefix based on Category or Live Status
    if category == "live" or is_live:
        color = 0xFF0000 # Red
        title_prefix = "🔴 LIVE MATCH"
    elif category == "upcoming":
        color = 0x3498DB # Blue
        title_prefix = "⏳ UPCOMING MATCH"
    elif category == "ended":
        color = 0x95A5A6 # Grey
        title_prefix = "🏁 ENDED MATCH"
    else:
        # Fallback logic
        color = 0xFF0000 if is_live else 0x3498DB
        title_prefix = "🏏 MATCH DETAILS"
    
    # Emojis & Headers
    emoji_status = config.EMOJI_GUIDE["status"]

    embed = discord.Embed(
        title=f"{title_prefix}: {match_name}",
        description=f"{emoji_status} *{status}*",
        color=color
    )
    
    # Add Score Fields
    embed.add_field(name=f"🟦 {team1}", value=f"```yaml\n{score1}\n```", inline=True)
    embed.add_field(name=f"🟥 {team2}", value=f"```yaml\n{score2}\n```", inline=True)
    
    embed.set_footer(text="SleepyCricketBot • Thoda late update ho toh gussa mat karna")
    
    return embed

def create_grouped_match_embed(matches, title, color):
    """
    Creates a single Embed listing multiple matches.
    """
    embed = discord.Embed(title=title, color=color)
    
    if not matches:
        embed.description = "No matches found in this category."
        return embed

    for match in matches:
        scores_list = match.get("scores", [])
        # Simplified score extraction for list view
        if len(scores_list) >= 1:
             s1 = scores_list[0].get("score", "-")
             t1 = scores_list[0].get("team", "?")
             score_str = f"{t1}: {s1}"
             if len(scores_list) >= 2:
                  s2 = scores_list[1].get("score", "-")
                  t2 = scores_list[1].get("team", "?")
                  score_str += f"\n{t2}: {s2}"
        else:
             score_str = "Waiting for toss..."

        match_name = match.get("match", "Match")
        status = match.get("status", "")
        
        # Format: 
        # Title: Match Name
        # Value: Team1: Score vs Team2: Score \n Status
        
        field_value = f"```{score_str}```\n*{status}*"
        embed.add_field(name=f"🏏 {match_name}", value=field_value, inline=False)
        
    embed.set_footer(text=f"Total: {len(matches)}")
    return embed
