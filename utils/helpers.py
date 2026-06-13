import discord, random
from datetime import datetime
from config import C_GOLD, FUNNY

def emb(title, desc="", color=C_GOLD):
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now())
    e.set_footer(text="🏦 YF BANK | عائلة يونان 👑")
    return e

def fmt(n):
    if n >= 1_000_000_000: return f"{n/1_000_000_000:.1f}B"
    if n >= 1_000_000:     return f"{n/1_000_000:.1f}M"
    if n >= 1_000:         return f"{n/1_000:.1f}K"
    return str(n)

def funny(key):
    return random.choice(FUNNY.get(key, ["🤔"]))

def get_rank(lvl):
    for threshold, name in reversed([
        (0,   "🪨 مبتدئ"),
        (10,  "🥉 تاجر"),
        (20,  "🥈 مستثمر"),
        (30,  "🥇 مليونير"),
        (50,  "💎 أسطورة"),
        (100, "👑 إله يوناني"),
    ]):
        if lvl >= threshold:
            return name
    return "🪨 مبتدئ"

def add_xp(data, coins_earned):
    from config import XP_PER_COIN
    xp_gain = max(1, int(coins_earned * XP_PER_COIN))
    data["xp"] += xp_gain
    leveled = False
    while data["xp"] >= data["level"] * 1000:
        data["xp"]    -= data["level"] * 1000
        data["level"] += 1
        leveled = True
    return leveled, xp_gain

def bar(cur, total, length=15):
    if total == 0: return "░" * length
    filled = int(length * cur / total)
    return "█" * filled + "░" * (length - filled)
