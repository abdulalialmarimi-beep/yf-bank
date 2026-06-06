"""
╔══════════════════════════════════════════════════════════════════╗
║  YF BANK - Yonan Family Discord Economy Bot                     ║
║  أقوى بوت اقتصادي في تاريخ ديسكورد                              ║
╚══════════════════════════════════════════════════════════════════╝
"""

import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
import random
import json
import os
from datetime import datetime, timedelta
from typing import Optional

BOT_TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_BOT_TOKEN_HERE")
COMMAND_PREFIX = "yf"
C_GOLD = 0xd4a843
C_GREEN = 0x4ade80
C_RED = 0xf87171
C_BLUE = 0x60a5fa
C_PINK = 0xff69b4
C_PURPLE = 0x9333ea
C_ORANGE = 0xf97316

DB_FILE = "yf_bank_data.json"


def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user(db, uid: str):
    if uid not in db:
        db[uid] = {
            "balance": 5000,
            "bank": 0,
            "level": 1,
            "xp": 0,
            "streak": 0,
            "last_daily": None,
            "total_earned": 0,
            "total_lost": 0,
            "total_gambled": 0,
            "properties": {
                "cars": 0,
                "stocks": 0,
                "lands": 0,
                "trains": 0,
                "phones": 0,
                "companies": 0,
                "servers": 0,
                "diamonds": 0,
            },
            "inventory": {},
            "married_to": None,
            "married_since": None,
            "dowry": 0,
            "divorce_count": 0,
            "last_divorce": None,
            "protection": None,
            "protection_expires": None,
            "rob_attempts": 0,
            "rob_success": 0,
            "rob_failed": 0,
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "jackpots": 0,
            "achievements": [],
            "gifts_received": 0,
            "gifts_sent": 0,
            "joined": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
        }
        save_db(db)
    return db[uid]


MARKET = {
    "bitcoin": {"name": "بيتكوين", "icon": "₿", "buy": 49000, "sell": 44000},
    "gold": {"name": "ذهب", "icon": "🥇", "buy": 5000, "sell": 4500},
    "diamond": {"name": "ألماس", "icon": "💎", "buy": 8200, "sell": 7400},
    "silver": {"name": "فضة", "icon": "🥈", "buy": 986, "sell": 887},
    "emerald": {"name": "زمرد", "icon": "💚", "buy": 5900, "sell": 5300},
    "ruby": {"name": "ياقوت", "icon": "❤️", "buy": 6300, "sell": 5700},
    "platinum": {"name": "بلاتين", "icon": "⚪", "buy": 15000, "sell": 13500},
    "oil": {"name": "نفط", "icon": "🛢️", "buy": 8000, "sell": 7200},
}

PROPERTIES = {
    "cars": {"name": "سيارات", "icon": "🚗", "price": 50000, "income": 5000, "desc": "تأجير سيارات فاخرة"},
    "stocks": {"name": "أسهم", "icon": "📊", "price": 10000, "income": 1000, "desc": "محفظة استثمارية"},
    "lands": {"name": "أراضي", "icon": "🏙️", "price": 100000, "income": 8000, "desc": "عقارات وتطوير"},
    "trains": {"name": "قطارات", "icon": "🚂", "price": 200000, "income": 15000, "desc": "خطوط نقل"},
    "phones": {"name": "هواتف", "icon": "📱", "price": 5000, "income": 500, "desc": "محل إلكترونيات"},
    "companies": {"name": "شركات", "icon": "💻", "price": 500000, "income": 30000, "desc": "إمبراطورية أعمال"},
    "servers": {"name": "سيرفرات", "icon": "🖥️", "price": 20000, "income": 2000, "desc": "استضافة سحابية"},
    "diamonds": {"name": "ألماس", "icon": "💎", "price": 50000, "income": 4000, "desc": "مناجم ألماس"},
}

GAMES = {
    "slots": {"name": "سلات", "icon": "🎰", "desc": "جاكبوت $50K!", "min": 50, "max": 5000, "color": C_GOLD},
    "dice": {"name": "نرد", "icon": "🎲", "desc": "الأعلى رقم يفوز", "min": 100, "max": 10000, "color": C_BLUE},
    "chicken": {"name": "دجاجة", "icon": "🐔", "desc": "كم تقدر تستمر؟", "min": 50, "max": 2000, "color": C_ORANGE},
    "colors": {"name": "ألوان", "icon": "🎨", "desc": "خمن اللون x2", "min": 50, "max": 5000, "color": C_PURPLE},
    "fruits": {"name": "فواكه", "icon": "🍎", "desc": "مطابقة الفواكه حتى x10", "min": 50, "max": 3000, "color": C_GREEN},
    "boxes": {"name": "صناديق", "icon": "📦", "desc": "افتح الصندوق!", "min": 100, "max": 10000, "color": C_BLUE},
    "wheel": {"name": "عجلة", "icon": "🎡", "desc": "دور العجلة حتى x10", "min": 100, "max": 50000, "color": C_PINK},
    "gamble": {"name": "قمار", "icon": "🃏", "desc": "50/50 كل شيء أو لا شيء", "min": 100, "max": 50000, "color": C_RED},
    "blackjack": {"name": "بلاك جاك", "icon": "🃏", "desc": "21 نقطة", "min": 100, "max": 10000, "color": C_GREEN},
    "crash": {"name": "تكس", "icon": "📈", "desc": "اطلع قبل ما ينهار!", "min": 50, "max": 5000, "color": C_ORANGE},
    "luck": {"name": "حظ", "icon": "🍀", "desc": "جرّب حظك حتى x10", "min": 10, "max": 1000, "color": C_GREEN},
}

ACHIEVEMENTS = {
    "first_win": {"name": "أول فوز", "desc": "اربح لعبتك الأولى", "reward": 100},
    "rich": {"name": "غني", "desc": "وصل لـ $100,000", "reward": 5000},
    "millionaire": {"name": "مليونير", "desc": "وصل لـ $1,000,000", "reward": 50000},
    "jackpot": {"name": "جاكبوت", "desc": "اربح الجاكبوت في السلات", "reward": 10000},
    "married": {"name": "متزوج", "desc": "تزوج بنجاح", "reward": 1000},
    "robber": {"name": "لص محترف", "desc": "نجح في 10 سرقات", "reward": 5000},
    "streak_7": {"name": "متسلسل", "desc": "سلسلة 7 أيام", "reward": 2000},
    "streak_30": {"name": "أسطوري", "desc": "سلسلة 30 يوم", "reward": 20000},
    "level_10": {"name": "نجم", "desc": "وصل للمستوى 10", "reward": 5000},
    "level_50": {"name": "إله", "desc": "وصل للمستوى 50", "reward": 100000},
    "properties_10": {"name": "مستثمر", "desc": "اشترِ 10 ممتلكات", "reward": 10000},
    "games_100": {"name": "لاعب محترف", "desc": "العب 100 لعبة", "reward": 5000},
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class YFBank(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)
        self.db = load_db()
        self.market = {k: v.copy() for k, v in MARKET.items()}

    async def setup_hook(self):
        self.market_updater.start()
        self.income_collector.start()

    @tasks.loop(minutes=30)
    async def market_updater(self):
        for item in self.market.values():
            change = random.uniform(-0.15, 0.15)
            item["buy"] = max(50, int(item["buy"] * (1 + change)))
            item["sell"] = max(25, int(item["sell"] * (1 + change)))
            if item["sell"] >= item["buy"]:
                item["sell"] = int(item["buy"] * 0.88)

    @tasks.loop(hours=24)
    async def income_collector(self):
        for uid, data in self.db.items():
            total_income = sum(
                data["properties"].get(k, 0) * prop["income"]
                for k, prop in PROPERTIES.items()
            )
            if total_income > 0:
                data["balance"] += total_income
                data["total_earned"] += total_income
        save_db(self.db)

    @market_updater.before_loop
    @income_collector.before_loop
    async def before_loops(self):
        await self.wait_until_ready()


bot = YFBank()


def emb(title: str, desc: str = "", color: int = C_GOLD):
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now())
    e.set_footer(text="YF BANK 2026 | عائلة يونان")
    return e


def get_rank(lvl: int) -> str:
    ranks = ["مبتدئ", "تاجر", "مستثمر", "مليونير", "أسطورة", "إله"]
    return ranks[min(lvl // 10, 5)]


def progress_bar(current: int, total: int, length: int = 15) -> str:
    filled = int(length * current / total)
    return "█" * filled + "░" * (length - filled)


def format_money(amount: int) -> str:
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"{amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{amount / 1_000:.1f}K"
    return str(amount)


def check_achievements(data: dict):
    new = []
    achieved = set(data.get("achievements", []))
    checks = [
        ("rich", data["balance"] + data["bank"] >= 100000),
        ("millionaire", data["balance"] + data["bank"] >= 1000000),
        ("married", data["married_to"] is not None),
        ("robber", data.get("rob_success", 0) >= 10),
        ("streak_7", data["streak"] >= 7),
        ("streak_30", data["streak"] >= 30),
        ("level_10", data["level"] >= 10),
        ("level_50", data["level"] >= 50),
        ("properties_10", sum(data["properties"].values()) >= 10),
        ("games_100", data["games_played"] >= 100),
    ]
    for key, condition in checks:
        if condition and key not in achieved:
            new.append(ACHIEVEMENTS[key])
            data["achievements"].append(key)
            data["balance"] += ACHIEVEMENTS[key]["reward"]
    return new


@bot.tree.command(name="balance", description="عرض الرصيد")
@app_commands.describe(user="مستخدم آخر (اختياري)")
async def balance_cmd(interaction: discord.Interaction, user: Optional[discord.User] = None):
    target = user or interaction.user
    data = get_user(bot.db, str(target.id))
    total = data["balance"] + data["bank"]
    xp_needed = data["level"] * 1000
    xp_progress = data["xp"] % xp_needed
    data["last_active"] = datetime.now().isoformat()
    save_db(bot.db)
    embed = emb(f"💳 محفظة — {target.display_name} {'👑' if data['level'] >= 30 else ''}", color=C_GOLD)
    embed.add_field(name="", value=f"## 💰 ${format_money(total)}", inline=False)
    embed.add_field(name="", value="الرصيد الكلي • عملات YF", inline=False)
    bar = progress_bar(xp_progress, xp_needed, 18)
    embed.add_field(
        name=f"⚡ المستوى {data['level']} — {get_rank(data['level'])}",
        value=f"`{bar}` {xp_progress / xp_needed * 100:.1f}%",
        inline=False,
    )
    embed.add_field(name="🏛️ البنك", value=f"${format_money(data['bank'])}", inline=True)
    embed.add_field(name="🪙 اليد", value=f"${format_money(data['balance'])}", inline=True)
    embed.add_field(name="📉 خسارة", value=f"${format_money(data.get('total_lost', 0))}", inline=True)
    embed.add_field(name="💼 ممتلكات", value=f"{sum(data['properties'].values())}", inline=True)
    embed.add_field(name="💎 جواهر", value=f"{sum(data.get('inventory', {}).values())}", inline=True)
    embed.add_field(name="🔥 سلسلة", value=f"{data['streak']} يوم", inline=True)
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="💸 تحويل", style=discord.ButtonStyle.primary))
    view.add_item(discord.ui.Button(label="🏛️ إيداع", style=discord.ButtonStyle.success))
    view.add_item(discord.ui.Button(label="📊 تداول", style=discord.ButtonStyle.secondary))
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name="daily", description="المكافأة اليومية")
async def daily_cmd(interaction: discord.Interaction):
    data = get_user(bot.db, str(interaction.user.id))
    now = datetime.now()
    if data["last_daily"]:
        last = datetime.fromisoformat(data["last_daily"])
        diff = now - last
        if diff < timedelta(hours=24):
            remaining = timedelta(hours=24) - diff
            h = int(remaining.total_seconds() // 3600)
            m = int((remaining.total_seconds() % 3600) // 60)
            embed = emb("⏳ المكافأة اليومية", f"لقد استلمت مكافأتك!\nارجع بعد **{h}س {m}د**", C_RED)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        if diff > timedelta(hours=48):
            data["streak"] = 1
        else:
            data["streak"] += 1
    else:
        data["streak"] = 1
    base = 1000
    streak_bonus = min(data["streak"] * 100, 5000)
    level_bonus = data["level"] * 50
    total = base + streak_bonus + level_bonus
    data["balance"] += total
    data["last_daily"] = now.isoformat()
    data["total_earned"] += total
    data["xp"] += 100
    while data["xp"] >= data["level"] * 1000:
        data["xp"] -= data["level"] * 1000
        data["level"] += 1
    new_ach = check_achievements(data)
    save_db(bot.db)
    embed = emb("🎁 تم استلام المكافأة!", color=C_GREEN)
    embed.add_field(name="💰 أساسية", value=f"${base:,}", inline=True)
    embed.add_field(name="🔥 سلسلة", value=f"${streak_bonus:,} (x{data['streak']})", inline=True)
    embed.add_field(name="⚡ مستوى", value=f"${level_bonus:,}", inline=True)
    embed.add_field(name="💎 إجمالي", value=f"**${total:,}**", inline=False)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=True)
    embed.add_field(name="🔥 سلسلة", value=f"**{data['streak']} أيام**", inline=True)
    if new_ach:
        embed.add_field(
            name="🎉 إنجاز جديد!",
            value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            inline=False,
        )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="top", description="أغنى المستخدمين")
async def top_cmd(interaction: discord.Interaction):
    embed = emb("🏆 أغنى المستخدمين — عائلة يونان", color=C_GOLD)
    users_data = [
        (m, d["balance"] + d["bank"], d["level"])
        for uid, d in bot.db.items()
        if (m := interaction.guild.get_member(int(uid)))
    ]
    users_data.sort(key=lambda x: x[1], reverse=True)
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    for i, (member, total, lvl) in enumerate(users_data[:10]):
        embed.add_field(
            name=f"{medals[i] if i < 3 else f'#{i+1}'} {member.display_name}",
            value=f"💰 ${format_money(total)} | ⚡ Lvl {lvl}",
            inline=False,
        )
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="💰 الأغنى", style=discord.ButtonStyle.primary))
    view.add_item(discord.ui.Button(label="📈 المستوى", style=discord.ButtonStyle.secondary))
    view.add_item(discord.ui.Button(label="💀 اللصوص", style=discord.ButtonStyle.danger))
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name="market", description="أسعار السوق الحية")
async def market_cmd(interaction: discord.Interaction):
    embed = emb("📊 سوق YF — الأسعار الحية", "تتغير كل 30 دقيقة", C_GOLD)
    for key, item in bot.market.items():
        original = MARKET[key]["buy"]
        change = ((item["buy"] - original) / original) * 100
        emoji = "🟢" if change >= 0 else "🔴"
        embed.add_field(
            name=f"{item['icon']} {item['name']}",
            value=f"{emoji} شراء: ${format_money(item['buy'])}\nبيع: ${format_money(item['sell'])}\nتغير: {change:+.2f}%",
            inline=True,
        )
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🛒 شراء", style=discord.ButtonStyle.success))
    view.add_item(discord.ui.Button(label="💰 بيع", style=discord.ButtonStyle.danger))
    view.add_item(discord.ui.Button(label="📦 مخزن", style=discord.ButtonStyle.secondary))
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name="games", description="قائمة الألعاب")
async def games_cmd(interaction: discord.Interaction):
    embed = emb("🎮 الألعاب — اختر لعبتك", "💎 💎 💎 جاكبوت! +$50,000 ✨", C_GOLD)
    for key, game in GAMES.items():
        embed.add_field(
            name=f"{game['icon']} {game['name']}",
            value=f"{game['desc']}\nحد: ${game['min']:,}-${game['max']:,}",
            inline=True,
        )
    select = discord.ui.Select(
        placeholder="🎮 اختر لعبة...",
        options=[
            discord.SelectOption(
                label=g["name"],
                description=f"{g['desc']} | ${g['min']:,}-${g['max']:,}",
                value=k,
                emoji=g["icon"],
            )
            for k, g in GAMES.items()
        ],
    )

    async def cb(i: discord.Interaction):
        g = GAMES[select.values[0]]
        e = emb(f"{g['icon']} {g['name']}", f"{g['desc']}\nحد الرهان: ${g['min']:,}-${g['max']:,}", g["color"])
        v = discord.ui.View()
        for amt in [100, 500, 1000, 5000]:
            if g["min"] <= amt <= g["max"]:
                v.add_item(discord.ui.Button(label=f"لعب ${amt:,}", style=discord.ButtonStyle.primary))
        v.add_item(discord.ui.Button(label="💰 كل شيء", style=discord.ButtonStyle.danger))
        await i.response.send_message(embed=e, view=v)

    select.callback = cb
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name="slots", description="آلة الحظ — جرب حظك!")
@app_commands.describe(bet="مبلغ الرهان ($50 - $5,000)")
async def slots_cmd(interaction: discord.Interaction, bet: int):
    data = get_user(bot.db, str(interaction.user.id))
    if bet < 50 or bet > 5000:
        await interaction.response.send_message("❌ الرهان: $50 - $5,000!", ephemeral=True)
        return
    if data["balance"] < bet:
        await interaction.response.send_message("❌ رصيدك لا يكفي!", ephemeral=True)
        return
    symbols = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🔔", "🎰"]
    weights = [25, 22, 18, 15, 8, 5, 4, 3]
    await interaction.response.defer()
    msg = await interaction.followup.send("🎰 يدور...")
    for _ in range(4):
        await asyncio.sleep(0.6)
        temp = random.choices(symbols, weights=weights, k=3)
        await msg.edit(content=f"🎰 | {temp[0]} | {temp[1]} | {temp[2]} | 🎰")
    result = random.choices(symbols, weights=weights, k=3)
    mult = 0
    if result[0] == result[1] == result[2]:
        mult = {"💎": 100, "7️⃣": 50, "🔔": 25, "🎰": 20}.get(result[0], 10)
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        mult = 2
    winnings = bet * mult
    if mult > 0:
        data["balance"] += winnings - bet
        data["total_earned"] += winnings - bet
        data["wins"] += 1
        if mult >= 50:
            data["jackpots"] += 1
        color = C_GREEN
        title = f"💎💎💎 جاكبوت!!! +${winnings:,}" if mult >= 50 else f"🎉 فزت بـ ${winnings:,}!"
    else:
        data["balance"] -= bet
        data["total_lost"] += bet
        data["losses"] += 1
        color = C_RED
        title = "😢 حظ سيئ!"
    data["games_played"] += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)
    embed = emb(title, color=color)
    embed.add_field(name="🎰 النتيجة", value=f"### | {result[0]} | {result[1]} | {result[2]} |", inline=False)
    embed.add_field(name="💵 الرهان", value=f"${bet:,}", inline=True)
    embed.add_field(name="📈 المضاعف", value=f"x{mult}", inline=True)
    embed.add_field(name="💰 الأرباح", value=f"${winnings:,}", inline=True)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=False)
    if new_ach:
        embed.add_field(
            name="🎉 إنجاز جديد!",
            value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            inline=False,
        )
    await msg.edit(content=None, embed=embed)


@bot.tree.command(name="wheel", description="عجلة الحظ — اربح حتى x10!")
@app_commands.describe(bet="مبلغ الرهان ($100 - $50,000)")
async def wheel_cmd(interaction: discord.Interaction, bet: int):
    data = get_user(bot.db, str(interaction.user.id))
    if bet < 100 or bet > 50000:
        await interaction.response.send_message("❌ الرهان: $100 - $50,000!", ephemeral=True)
        return
    if data["balance"] < bet:
        await interaction.response.send_message("❌ رصيدك لا يكفي!", ephemeral=True)
        return
    segments = [
        ("0x 💀", 0.0, "💀", C_RED),
        ("0.5x 🔴", 0.5, "🔴", C_RED),
        ("0.8x ⚫", 0.8, "⚫", C_ORANGE),
        ("1x 🔵", 1.0, "🔵", C_BLUE),
        ("1.5x 🟢", 1.5, "🟢", C_GREEN),
        ("2x 💚", 2.0, "💚", C_GREEN),
        ("3x 🌟", 3.0, "🌟", C_GOLD),
        ("5x ✨", 5.0, "✨", C_GOLD),
        ("10x 💎", 10.0, "💎", C_PURPLE),
    ]
