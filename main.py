"""
╔══════════════════════════════════════════════════════════════════╗
║  YF BANK - Yonan Family Discord Economy Bot                     ║
║  أقوى بوت اقتصادي في تاريخ ديسكورد - عائلة يونان               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import os
from datetime import datetime, timedelta
from typing import Optional

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
if not BOT_TOKEN:
    print("❌ خطأ: ما في توكن!")
    exit(1)

COMMAND_PREFIX = "-"
C_GOLD=0xd4a843; C_GREEN=0x4ade80; C_RED=0xf87171; C_BLUE=0x60a5fa
C_PINK=0xff69b4; C_PURPLE=0x9333ea; C_ORANGE=0xf97316; C_CYAN=0x22d3ee
DB_FILE = "yf_bank_data.json"

IMAGES = {
    "logo":None,"bank":None,"balance":None,"daily":None,"top":None,
    "broke":None,"transfer":None,"market":None,"properties":None,
    "games":None,"slots":None,"wheel":None,"blackjack":None,"crash":None,
    "dice":None,"chicken":None,"colors":None,"fruits":None,"boxes":None,
    "gamble":None,"luck":None,"marry":None,"divorce":None,"marry_bot":None,
    "marry_self":None,"rob":None,"rob_fail":None,"protection":None,
    "help":None,"commands":None,"achievement":None,"jackpot":None,"level_up":None,
}

FUNNY_MESSAGES = {
    "broke":["يا اخي حتى الفقر ما يجي فخامة زيك!","يونان فاملي ما يعرف الفقر! بس انت عضو شرفي في نادي الفقراء!","رصيدك صفر؟ حتى المهرجين عندهم فلوس اكثر منك!"],
    "marry_bot":["يا حبيبي تبي تتزوج بوت؟","البوت قال: انا ما ابي اتزوج انسان بطيء المعالجة!"],
    "marry_self":["تبي تتزوج نفسك؟ حتى المراة تستحي منك!","حتى نفسك ما تبي تتزوجك!"],
    "rob_self":["تبي تسرق نفسك؟ يا ذكي! نفسك ما عندها فلوس اصلا!"],
    "rob_poor":["تبي تسرق فقير؟ حتى اللصوص عندهم اخلاق!","الضحية فقير زيك! روحوا افتحوا نادي الفقراء!"],
    "transfer_self":["تحول لنفسك؟ الفلوس راحت وجت لنفس المحفظة!"],
    "divorce_cooldown":["يا ولد كم مرة تبي تطلق؟ يونان فاملي مش محكمة!","روح استقر شوي!"],
    "already_married":["يا حبيبي انت متزوج! يونان فاملي مو مسلسل تركي!"],
    "partner_married":["الشخص متزوج! يونان فاملي ما يقبل الخيانة!"],
    "not_married":["انت مو متزوج! وش بتطلق؟ نفسك؟"],
    "rob_fail":["الشرطة قبضت عليك! يونان فاملي ما يحمي اللصوص الفاشلين!","انكشفت! روح اشتغل شريف!"],
    "rob_success":["يونان فاملي يفتخر بك! لص محترف!","مسكتها! يونان فاملي يسلم عليك!"],
    "daily_streak":["يا سلام! سلسلة يونان فاملي قوية! {streak} ايام!","مستمر يا بطل!"],
    "level_up":["يونان فاملي تهنئك! مستوى جديد!","صاروخ يونان فاملي!"],
    "jackpot":["يا ولد! جاكبوت يونان فاملي! انت مليونير!","صرت غني! يونان فاملي تبغى قرض منك!"],
    "protection_active":["عندك حماية يونان فاملي! ما حد يقدر يلمسك!"],
    "buy_property":["صار عندك عقار! يونان فاملي تصير رجل اعمال!","استثمار ذكي!"],
}

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE,"r",encoding="utf-8") as f: return json.load(f)
    return {}
"""
╔══════════════════════════════════════════════════════════════════╗
║  YF BANK - Yonan Family Discord Economy Bot                     ║
║  أقوى بوت اقتصادي في تاريخ ديسكورد - عائلة يونان               ║
║  النسخة المطورة - كل الأوامر بالعربية مع صور وفكاهة             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import discord
from discord.ext import commands, tasks
import asyncio
import random
import json
import os
from datetime import datetime, timedelta
from typing import Optional

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
if not BOT_TOKEN:
    print("❌ خطأ: ما في توكن!")
    print("📝 روح لـ Tools → Secrets في Replit")
    print("🔑 أضف: DISCORD_TOKEN = توكن_البوت")
    exit(1)

COMMAND_PREFIX = "-"

C_GOLD   = 0xd4a843
C_GREEN  = 0x4ade80
C_RED    = 0xf87171
C_BLUE   = 0x60a5fa
C_PINK   = 0xff69b4
C_PURPLE = 0x9333ea
C_ORANGE = 0xf97316
C_CYAN   = 0x22d3ee

DB_FILE = "yf_bank_data.json"

IMAGES = {
    "logo": None, "bank": None, "balance": None, "daily": None,
    "top": None, "broke": None, "transfer": None, "market": None,
    "properties": None, "games": None, "slots": None, "wheel": None,
    "blackjack": None, "crash": None, "dice": None, "chicken": None,
    "colors": None, "fruits": None, "boxes": None, "gamble": None,
    "luck": None, "marry": None, "divorce": None, "marry_bot": None,
    "marry_self": None, "rob": None, "rob_fail": None, "protection": None,
    "help": None, "commands": None, "achievement": None, "jackpot": None,
    "level_up": None,
}

FUNNY_MESSAGES = {
    "broke": [
        "يا اخي حتى الفقر ما يجي فخامة زيك! محفظتك صارت تعيش في خيمة!",
        "يونان فاملي ما يعرف الفقر! بس انت واضح انك عضو شرفي في نادي الفقراء!",
        "حتى الريال يونان يبكي لما يشوف رصيدك! روح اشتغل شوي يا بطل!",
        "رصيدك صفر؟ حتى المهرجين في السيرك عندهم فلوس اكثر منك!",
        "يا ولد حتى الجثة في القبر عندها اكثر من رصيدك!",
    ],
    "marry_bot":  ["يا حبيبي تبي تتزوج بوت؟ وش نوع العلاقة هذي؟", "البوت قال: انا ما ابي اتزوج انسان بطيء المعالجة!"],
    "marry_self": ["تبي تتزوج نفسك؟ حتى المراة تستحي منك يا نرجسي!", "حتى نفسك ما تبي تتزوجك! فكر فيها شوي!"],
    "rob_self":   ["تبي تسرق نفسك؟ يا ذكي! روح سرق غيرك، نفسك ما عندها فلوس اصلا!"],
    "rob_poor":   ["تبي تسرق فقير؟ حتى اللصوص في يونان فاملي عندهم اخلاق!", "الضحية فقير زيك! روحوا افتحوا نادي الفقراء مع بعض!"],
    "transfer_self": ["تحول لنفسك؟ يا بطل! الفلوس راحت وجت... لنفس المحفظة!"],
    "divorce_cooldown": ["يا ولد كم مرة تبي تطلق؟ يونان فاملي مش محكمة استئناف!", "روح استقر شوي!"],
    "already_married":  ["يا حبيبي انت متزوج! وش تبي؟ زوجة ثانية؟ يونان فاملي مو مسلسل تركي!"],
    "partner_married":  ["الشخص متزوج! تبي تخرب بيته؟ يونان فاملي ما يقبل الخيانة!"],
    "not_married":      ["انت مو متزوج! وش بتطلق؟ نفسك؟"],
    "rob_fail":    ["الشرطة قبضت عليك! يونان فاملي ما يحمي اللصوص الفاشلين!", "انكشفت! روح اشتغل شريف افضل لك!"],
    "rob_success": ["يونان فاملي يفتخر بك! لص محترف وبارع!", "مسكتها! يونان فاملي يسلم عليك يا لص المحترفين!"],
    "daily_streak": ["يا سلام! سلسلة يونان فاملي قوية! {streak} ايام!", "مستمر يا بطل! عائلة يونان فخورة فيك!"],
    "level_up":  ["يونان فاملي تهنئك! وصلت لمستوى جديد!", "صاروخ يونان فاملي! مستوى جديد!"],
    "jackpot":   ["يا ولد! جاكبوت يونان فاملي! انت مليونير الان!", "صرت غني! يونان فاملي تبغى قرض منك!"],
    "protection_active": ["عندك حماية يونان فاملي! ما حد يقدر يلمسك!"],
    "buy_property":      ["صار عندك عقار! يونان فاملي تصير رجل اعمال!", "استثمار ذكي! يونان فاملي تفتخر فيك!"],
}

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
            "balance": 5000, "bank": 0, "level": 1, "xp": 0, "streak": 0,
            "last_daily": None, "total_earned": 0, "total_lost": 0, "total_gambled": 0,
            "properties": {"cars": 0, "stocks": 0, "lands": 0, "trains": 0,
                           "phones": 0, "companies": 0, "servers": 0, "diamonds": 0},
            "inventory": {}, "married_to": None, "married_since": None, "dowry": 0,
            "divorce_count": 0, "last_divorce": None, "protection": None,
            "protection_expires": None, "rob_attempts": 0, "rob_success": 0,
            "rob_failed": 0, "games_played": 0, "wins": 0, "losses": 0,
            "jackpots": 0, "achievements": [], "gifts_received": 0, "gifts_sent": 0,
            "joined": datetime.now().isoformat(), "last_active": datetime.now().isoformat(),
        }
        save_db(db)
    return db[uid]

MARKET = {
    "bitcoin":  {"name": "بيتكوين", "icon": "₿",  "buy": 49000, "sell": 44000},
    "gold":     {"name": "ذهب",     "icon": "🥇", "buy": 5000,  "sell": 4500},
    "diamond":  {"name": "الماس",   "icon": "💎", "buy": 8200,  "sell": 7400},
    "silver":   {"name": "فضة",     "icon": "🥈", "buy": 986,   "sell": 887},
    "emerald":  {"name": "زمرد",    "icon": "💚", "buy": 5900,  "sell": 5300},
    "ruby":     {"name": "ياقوت",   "icon": "❤️", "buy": 6300,  "sell": 5700},
    "platinum": {"name": "بلاتين",  "icon": "⚪", "buy": 15000, "sell": 13500},
    "oil":      {"name": "نفط",     "icon": "🛢️", "buy": 8000,  "sell": 7200},
}

PROPERTIES = {
    "cars":      {"name": "سيارات",  "icon": "🚗", "price": 50000,  "income": 5000,  "desc": "تأجير سيارات فاخرة"},
    "stocks":    {"name": "أسهم",    "icon": "📊", "price": 10000,  "income": 1000,  "desc": "محفظة استثمارية"},
    "lands":     {"name": "أراضي",   "icon": "🏙️", "price": 100000, "income": 8000,  "desc": "عقارات وتطوير"},
    "trains":    {"name": "قطارات",  "icon": "🚂", "price": 200000, "income": 15000, "desc": "خطوط نقل"},
    "phones":    {"name": "هواتف",   "icon": "📱", "price": 5000,   "income": 500,   "desc": "محل إلكترونيات"},
    "companies": {"name": "شركات",   "icon": "💻", "price": 500000, "income": 30000, "desc": "إمبراطورية أعمال"},
    "servers":   {"name": "سيرفرات","icon": "🖥️", "price": 20000,  "income": 2000,  "desc": "استضافة سحابية"},
    "diamonds":  {"name": "الماس",   "icon": "💎", "price": 50000,  "income": 4000,  "desc": "مناجم الماس"},
}

GAMES = {
    "slots":     {"name": "سلات",     "icon": "🎰", "desc": "جاكبوت 50K!",             "min": 50,  "max": 5000,  "color": C_GOLD,   "image": "slots"},
    "dice":      {"name": "نرد",      "icon": "🎲", "desc": "الأعلى رقم يفوز",         "min": 100, "max": 10000, "color": C_BLUE,   "image": "dice"},
    "chicken":   {"name": "دجاجة",    "icon": "🐔", "desc": "كم تقدر تستمر؟",          "min": 50,  "max": 2000,  "color": C_ORANGE, "image": "chicken"},
    "colors":    {"name": "ألوان",    "icon": "🎨", "desc": "خمّن اللون x2",            "min": 50,  "max": 5000,  "color": C_PURPLE, "image": "colors"},
    "fruits":    {"name": "فواكه",    "icon": "🍎", "desc": "مطابقة الفواكه حتى x10",  "min": 50,  "max": 3000,  "color": C_GREEN,  "image": "fruits"},
    "boxes":     {"name": "صناديق",   "icon": "📦", "desc": "افتح الصندوق!",            "min": 100, "max": 10000, "color": C_BLUE,   "image": "boxes"},
    "wheel":     {"name": "عجلة",     "icon": "🎡", "desc": "دور العجلة حتى x10",      "min": 100, "max": 50000, "color": C_PINK,   "image": "wheel"},
    "gamble":    {"name": "قمار",     "icon": "🃏", "desc": "50/50 كل شيء أو لا شيء", "min": 100, "max": 50000, "color": C_RED,    "image": "gamble"},
    "blackjack": {"name": "بلاك جاك","icon": "🃏", "desc": "21 نقطة",                  "min": 100, "max": 10000, "color": C_GREEN,  "image": "blackjack"},
    "crash":     {"name": "تكس",      "icon": "📈", "desc": "اطلع قبل ما ينهار!",      "min": 50,  "max": 5000,  "color": C_ORANGE, "image": "crash"},
    "luck":      {"name": "حظ",       "icon": "🍀", "desc": "جرب حظك حتى x10",         "min": 10,  "max": 1000,  "color": C_GREEN,  "image": "luck"},
}

ACHIEVEMENTS = {
    "first_win":    {"name": "أول فوز",      "desc": "اربح لعبتك الأولى",    "reward": 100},
    "rich":         {"name": "غني",           "desc": "وصل لـ 100,000",       "reward": 5000},
    "millionaire":  {"name": "مليونير",       "desc": "وصل لـ 1,000,000",     "reward": 50000},
    "jackpot":      {"name": "جاكبوت",        "desc": "اربح الجاكبوت في السلات", "reward": 10000},
    "married":      {"name": "متزوج",         "desc": "تزوج بنجاح",           "reward": 1000},
    "robber":       {"name": "لص محترف",      "desc": "نجح في 10 سرقات",      "reward": 5000},
    "streak_7":     {"name": "متسلسل",        "desc": "سلسلة 7 أيام",         "reward": 2000},
    "streak_30":    {"name": "أسطوري",        "desc": "سلسلة 30 يوم",         "reward": 20000},
    "level_10":     {"name": "نجم",           "desc": "وصل للمستوى 10",       "reward": 5000},
    "level_50":     {"name": "إله",           "desc": "وصل للمستوى 50",       "reward": 100000},
    "properties_10":{"name": "مستثمر",       "desc": "اشترِ 10 ممتلكات",     "reward": 10000},
    "games_100":    {"name": "لاعب محترف",   "desc": "العب 100 لعبة",         "reward": 5000},
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
            item["buy"]  = max(50, int(item["buy"]  * (1 + change)))
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
                data["balance"]      += total_income
                data["total_earned"] += total_income
        save_db(self.db)

    @market_updater.before_loop
    @income_collector.before_loop
    async def before_loops(self):
        await self.wait_until_ready()

bot = YFBank()

def emb(title, desc="", color=C_GOLD, image_key=None, thumbnail_key=None):
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now())
    logo = IMAGES.get("logo")
    if logo:
        e.set_footer(text="YF BANK 2026 | عائلة يونان", icon_url=logo)
    else:
        e.set_footer(text="YF BANK 2026 | عائلة يونان")
    if image_key and IMAGES.get(image_key):
        e.set_image(url=IMAGES[image_key])
    if thumbnail_key and IMAGES.get(thumbnail_key):
        e.set_thumbnail(url=IMAGES[thumbnail_key])
    return e

def get_rank(lvl):
    ranks = ["مبتدئ", "تاجر", "مستثمر", "مليونير", "أسطورة", "إله يوناني"]
    return ranks[min(lvl // 10, 5)]

def progress_bar(current, total, length=15):
    if total == 0:
        return "░" * length
    filled = int(length * current / total)
    return "█" * filled + "░" * (length - filled)

def format_money(amount):
    if amount >= 1_000_000_000: return f"{amount/1_000_000_000:.1f}B"
    if amount >= 1_000_000:     return f"{amount/1_000_000:.1f}M"
    if amount >= 1_000:         return f"{amount/1_000:.1f}K"
    return str(amount)

def get_funny(key, **kwargs):
    msgs = FUNNY_MESSAGES.get(key, ["🤔"])
    return random.choice(msgs).format(**kwargs)

def check_achievements(data):
    new, achieved = [], set(data.get("achievements", []))
    checks = [
        ("first_win",    data.get("wins", 0) >= 1),
        ("rich",         data["balance"] + data["bank"] >= 100_000),
        ("millionaire",  data["balance"] + data["bank"] >= 1_000_000),
        ("married",      data["married_to"] is not None),
        ("robber",       data.get("rob_success", 0) >= 10),
        ("streak_7",     data["streak"] >= 7),
        ("streak_30",    data["streak"] >= 30),
        ("level_10",     data["level"] >= 10),
        ("level_50",     data["level"] >= 50),
        ("properties_10",sum(data["properties"].values()) >= 10),
        ("games_100",    data["games_played"] >= 100),
    ]
    for key, condition in checks:
        if condition and key not in achieved:
            new.append(ACHIEVEMENTS[key])
            data["achievements"].append(key)
            data["balance"] += ACHIEVEMENTS[key]["reward"]
    return new

def add_ach_field(embed, new_ach):
    if new_ach:
        embed.add_field(
            name="🏆 إنجاز جديد!",
            value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            inline=False,
                             ) 
@bot.command(name="رصيد")
async def balance_cmd(ctx, user: Optional[discord.User] = None):
    target = user or ctx.author
    data   = get_user(bot.db, str(target.id))
    total  = data["balance"] + data["bank"]
    xp_needed   = data["level"] * 1000
    xp_progress = data["xp"] % xp_needed if xp_needed else 0
    data["last_active"] = datetime.now().isoformat()
    save_db(bot.db)

    funny_note = f"\n\n{get_funny('broke')}" if total < 1000 else ""
    embed = emb(
        f"محفظة — {target.display_name} {'👑' if data['level'] >= 30 else ''}",
        f"## 💰 ${format_money(total)}\nالرصيد الكلي • عملات YF{funny_note}",
        C_GOLD, image_key="balance"
    )
    bar = progress_bar(xp_progress, xp_needed, 18)
    pct = f"{xp_progress / xp_needed * 100:.1f}%" if xp_needed else "0%"
    embed.add_field(name=f"⚡ المستوى {data['level']} — {get_rank(data['level'])}", value=f"`{bar}` {pct}", inline=False)
    embed.add_field(name="🏛️ البنك",    value=f"${format_money(data['bank'])}",                          inline=True)
    embed.add_field(name="🪙 اليد",     value=f"${format_money(data['balance'])}",                       inline=True)
    embed.add_field(name="📉 خسارة",    value=f"${format_money(data.get('total_lost', 0))}",             inline=True)
    embed.add_field(name="💼 ممتلكات",  value=f"{sum(data['properties'].values())}",                     inline=True)
    embed.add_field(name="💎 جواهر",    value=f"{sum(data.get('inventory', {}).values())}",              inline=True)
    embed.add_field(name="🔥 سلسلة",   value=f"{data['streak']} يوم",                                    inline=True)
    await ctx.send(embed=embed)


@bot.command(name="يومي")
async def daily_cmd(ctx):
    data = get_user(bot.db, str(ctx.author.id))
    now  = datetime.now()
    if data["last_daily"]:
        diff = now - datetime.fromisoformat(data["last_daily"])
        if diff < timedelta(hours=24):
            rem = timedelta(hours=24) - diff
            h, m = int(rem.total_seconds()//3600), int((rem.total_seconds()%3600)//60)
            await ctx.send(embed=emb("⏳ المكافأة اليومية", f"{get_funny('broke')}\n\nارجع بعد **{h}س {m}د** ⏰", C_RED, image_key="broke"))
            return
        data["streak"] = 1 if diff > timedelta(hours=48) else data["streak"] + 1
    else:
        data["streak"] = 1

    base         = 1000
    streak_bonus = min(data["streak"] * 100, 5000)
    level_bonus  = data["level"] * 50
    total        = base + streak_bonus + level_bonus
    data["balance"]      += total
    data["last_daily"]    = now.isoformat()
    data["total_earned"] += total
    data["xp"]           += 100

    while data["xp"] >= data["level"] * 1000:
        data["xp"]    -= data["level"] * 1000
        data["level"] += 1

    new_ach = check_achievements(data)
    save_db(bot.db)

    embed = emb("🎁 تم استلام المكافأة!", color=C_GREEN, image_key="daily")
    embed.add_field(name="💰 أساسية", value=f"${base:,}",                             inline=True)
    embed.add_field(name="🔥 سلسلة",  value=f"${streak_bonus:,} (x{data['streak']})", inline=True)
    embed.add_field(name="⚡ مستوى",  value=f"${level_bonus:,}",                       inline=True)
    embed.add_field(name="💎 إجمالي", value=f"**${total:,}**",                         inline=False)
    embed.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}",                   inline=True)
    embed.add_field(name="🔥 سلسلة",  value=f"**{data['streak']} أيام**",              inline=True)
    add_ach_field(embed, new_ach)
    await ctx.send(embed=embed)


@bot.command(name="مطنوخين")
async def top_cmd(ctx):
    if not bot.db:
        await ctx.send("❌ ما في بيانات!"); return
    sorted_users = sorted(
        bot.db.items(),
        key=lambda x: x[1].get("balance", 0) + x[1].get("bank", 0),
        reverse=True
    )[:10]
    embed = emb("🏆 أغنى أعضاء يونان فاملي", "المطنوخين العشرة الأوائل! 👑", C_GOLD, image_key="top")
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    for i, (uid, data) in enumerate(sorted_users):
        try:
            user = await bot.fetch_user(int(uid))
            name = user.display_name
        except:
            name = f"مستخدم {uid[:6]}"
        total = data.get("balance", 0) + data.get("bank", 0)
        embed.add_field(
            name=f"{medals[i]} {name}",
            value=f"${format_money(total)} | مستوى {data.get('level',1)}",
            inline=False
        )
    await ctx.send(embed=embed)


@bot.command(name="سوق")
async def market_cmd(ctx):
    embed = emb("📊 سوق يونان فاملي الحي", "الأسعار تتغير كل 30 دقيقة! 📈", C_CYAN, image_key="market")
    for key, item in bot.market.items():
        embed.add_field(
            name=f"{item['icon']} {item['name']}",
            value=f"شراء: **${item['buy']:,}**\nبيع: **${item['sell']:,}**\n`-شراء {key} 1`",
            inline=True,
        )
    await ctx.send(embed=embed)


@bot.command(name="شراء")
async def buy_cmd(ctx, item_key: str, amount: int = 1):
    if item_key not in bot.market:
        await ctx.send(f"❌ ما في سلعة اسمها `{item_key}`! استخدم `-سوق` للقائمة.")
        return
    data      = get_user(bot.db, str(ctx.author.id))
    item      = bot.market[item_key]
    total_cost = item["buy"] * amount
    if data["balance"] < total_cost:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return
    data["balance"] -= total_cost
    data["inventory"][item_key] = data["inventory"].get(item_key, 0) + amount
    save_db(bot.db)
    await ctx.send(embed=emb("✅ تم الشراء!", f"اشتريت **{amount}x {item['name']}** بـ **${total_cost:,}**\nرصيدك: ${data['balance']:,}", C_GREEN))


@bot.command(name="بيع")
async def sell_cmd(ctx, item_key: str, amount: int = 1):
    if item_key not in bot.market:
        await ctx.send(f"❌ ما في سلعة اسمها `{item_key}`!")
        return
    data  = get_user(bot.db, str(ctx.author.id))
    owned = data["inventory"].get(item_key, 0)
    if owned < amount:
        await ctx.send(f"❌ ما عندك كافي! عندك {owned} فقط.")
        return
    item       = bot.market[item_key]
    total_earn = item["sell"] * amount
    data["inventory"][item_key] -= amount
    data["balance"]      += total_earn
    data["total_earned"] += total_earn
    save_db(bot.db)
    await ctx.send(embed=emb("✅ تم البيع!", f"بعت **{amount}x {item['name']}** بـ **${total_earn:,}**\nرصيدك: ${data['balance']:,}", C_GREEN))


@bot.command(name="إيداع")
async def deposit_cmd(ctx, amount: int):
    data = get_user(bot.db, str(ctx.author.id))
    if amount < 100:
        await ctx.send("❌ الحد الأدنى $100!"); return
    if data["balance"] < amount:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return
    data["balance"] -= amount
    data["bank"]    += amount
    save_db(bot.db)
    embed = emb("🏛️ إيداع ناجح!", f"تم إيداع **${amount:,}** في البنك ✅", C_GREEN, image_key="bank")
    embed.add_field(name="🪙 اليد", value=f"${data['balance']:,}", inline=True)
    embed.add_field(name="🏛️ البنك",value=f"${data['bank']:,}",    inline=True)
    await ctx.send(embed=embed)


@bot.command(name="سحب")
async def withdraw_cmd(ctx, amount: int):
    data = get_user(bot.db, str(ctx.author.id))
    if amount < 100:
        await ctx.send("❌ الحد الأدنى $100!"); return
    if data["bank"] < amount:
        await ctx.send(embed=emb("❌ فلوسك في البنك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return
    data["bank"]    -= amount
    data["balance"] += amount
    save_db(bot.db)
    embed = emb("🏛️ سحب ناجح!", f"تم سحب **${amount:,}** من البنك ✅", C_GREEN, image_key="bank")
    embed.add_field(name="🪙 اليد", value=f"${data['balance']:,}", inline=True)
    embed.add_field(name="🏛️ البنك",value=f"${data['bank']:,}",    inline=True)
    await ctx.send(embed=embed)


@bot.command(name="تحويل")
async def transfer_cmd(ctx, user: discord.User, amount: int):
    if user.id == ctx.author.id:
        await ctx.send(embed=emb("🤣 يا حبيبي!", get_funny("transfer_self"), C_RED, image_key="transfer")); return
    if amount < 100:
        await ctx.send("❌ الحد الأدنى $100!"); return
    data   = get_user(bot.db, str(ctx.author.id))
    target = get_user(bot.db, str(user.id))
    if data["balance"] < amount:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return
    data["balance"]        -= amount
    target["balance"]      += amount
    data["gifts_sent"]     += 1
    target["gifts_received"] += 1
    save_db(bot.db)
    embed = emb("💸 تحويل يوناني ناجح!", f"{ctx.author.mention} → {user.mention}\nالمبلغ: **${amount:,}** 💰", C_GREEN, image_key="transfer")
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    await ctx.send(embed=embed)
@bot.command(name="ألعاب")
async def games_cmd(ctx):
    embed = emb("🎮 ألعاب يونان فاملي", "💎 جاكبوت! +$50,000 ✨\nاختر لعبتك يا بطل!", C_GOLD, image_key="games")
    for key, game in GAMES.items():
        embed.add_field(
            name=f"{game['icon']} {game['name']}",
            value=f"{game['desc']}\nحد: `${game['min']:,}-${game['max']:,}`",
            inline=True,
        )
    embed.add_field(name="💡 كيف تلعب؟", value="`-سلات 500` أو `-عجلة 1000` أو `-بلاكجاك 200`", inline=False)
    await ctx.send(embed=embed)


@bot.command(name="سلات")
async def slots_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 50 or bet > 5000:
        await ctx.send("❌ الرهان: $50 - $5,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    symbols = ["🍒","🍋","🍊","🍇","💎","7️⃣","🔔","🎰"]
    weights = [25, 22, 18, 15,  8,   5,   4,   3]

    msg = await ctx.send("🎰 يدور...")
    for _ in range(4):
        await asyncio.sleep(0.6)
        t = random.choices(symbols, weights=weights, k=3)
        await msg.edit(content=f"🎰 | {t[0]} | {t[1]} | {t[2]} | 🎰")

    result = random.choices(symbols, weights=weights, k=3)
    mult   = 0
    if result[0] == result[1] == result[2]:
        mult = {"💎": 100, "7️⃣": 50, "🔔": 25, "🎰": 20}.get(result[0], 10)
    elif len(set(result)) < 3:
        mult = 2

    winnings = bet * mult
    if mult > 0:
        data["balance"]      += winnings - bet
        data["total_earned"] += winnings - bet
        data["wins"]         += 1
        if mult >= 50:
            data["jackpots"] += 1
        color   = C_GREEN
        title   = get_funny("jackpot") if mult >= 50 else f"🎉 فزت بـ ${winnings:,}!"
        img_key = "jackpot" if mult >= 50 else "slots"
    else:
        data["balance"]    -= bet
        data["total_lost"] += bet
        data["losses"]     += 1
        color, title, img_key = C_RED, "😢 حظ سيئ!", "slots"

    data["games_played"]  += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)

    embed = emb(title, color=color, image_key=img_key)
    embed.add_field(name="🎰 النتيجة", value=f"| {result[0]} | {result[1]} | {result[2]} |", inline=False)
    embed.add_field(name="💵 الرهان",  value=f"${bet:,}",       inline=True)
    embed.add_field(name="📈 مضاعف",   value=f"x{mult}",         inline=True)
    embed.add_field(name="💰 الأرباح", value=f"${winnings:,}",  inline=True)
    embed.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}", inline=False)
    add_ach_field(embed, new_ach)
    await msg.edit(content=None, embed=embed)


@bot.command(name="عجلة")
async def wheel_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 100 or bet > 50000:
        await ctx.send("❌ الرهان: $100 - $50,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    segments = [
        ("0x 💀",  0.0,  "💀", C_RED),
        ("0.5x 🔴",0.5,  "🔴", C_RED),
        ("0.8x ⚫",0.8,  "⚫", C_ORANGE),
        ("1x 🔵",  1.0,  "🔵", C_BLUE),
        ("1.5x 🟢",1.5,  "🟢", C_GREEN),
        ("2x 💚",  2.0,  "💚", C_GREEN),
        ("3x 🌟",  3.0,  "🌟", C_GOLD),
        ("5x ✨",  5.0,  "✨", C_GOLD),
        ("10x 💎", 10.0, "💎", C_PURPLE),
    ]
    weights = [8,12,15,20,18,12,8,5,2]

    msg = await ctx.send("🎡 تدور العجلة...")
    for _ in range(5):
        t = random.choice(segments)
        await asyncio.sleep(0.5)
        await msg.edit(content=f"🎡 → {t[2]} {t[0]} ← 🎡")
    await asyncio.sleep(1)

    label, mult, emoji, color = random.choices(segments, weights=weights)[0]
    winnings = int(bet * mult)

    if mult > 1:
        data["balance"]      += winnings - bet
        data["total_earned"] += winnings - bet
        data["wins"] += 1
        text = f"🎉 ربحت **${winnings:,}**!"
    elif mult == 1:
        color = C_BLUE
        text  = f"😊 استردت **${winnings:,}**"
    elif mult > 0:
        loss = bet - winnings
        data["balance"]    -= loss
        data["total_lost"] += loss
        text  = f"😢 خسرت **${loss:,}**"
        color = C_ORANGE
    else:
        data["balance"]    -= bet
        data["total_lost"] += bet
        data["losses"] += 1
        text = f"💀 خسرت كل شيء! **-${bet:,}**"

    data["games_played"]  += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)

    embed = emb(f"🎡 عجلة الحظ — {label}", text, color, image_key="wheel")
    embed.add_field(name="💵 الرهان",  value=f"${bet:,}",      inline=True)
    embed.add_field(name="📈 مضاعف",   value=f"x{mult}",        inline=True)
    embed.add_field(name="💰 الأرباح", value=f"${winnings:,}", inline=True)
    embed.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}", inline=False)
    add_ach_field(embed, new_ach)
    await msg.edit(content=None, embed=embed)


@bot.command(name="نرد")
async def dice_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 100 or bet > 10000:
        await ctx.send("❌ الرهان: $100 - $10,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    msg = await ctx.send("🎲 يرمي النرد...")
    await asyncio.sleep(1.5)

    player_roll = random.randint(1, 6)
    bot_roll    = random.randint(1, 6)

    if player_roll > bot_roll:
        data["balance"]      += bet
        data["total_earned"] += bet
        data["wins"] += 1
        color = C_GREEN
        result_text = f"🎉 فزت! {player_roll} > {bot_roll}"
        winnings = bet * 2
    elif player_roll < bot_roll:
        data["balance"]    -= bet
        data["total_lost"] += bet
        data["losses"] += 1
        color = C_RED
        result_text = f"😢 خسرت! {player_roll} < {bot_roll}"
        winnings = 0
    else:
        color = C_BLUE
        result_text = f"🤝 تعادل! {player_roll} = {bot_roll}"
        winnings = bet

    data["games_played"]  += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)

    embed = emb(f"🎲 نرد — {result_text}", color=color, image_key="dice")
    embed.add_field(name="🎲 أنت",   value=f"**{player_roll}**", inline=True)
    embed.add_field(name="🤖 البوت", value=f"**{bot_roll}**",    inline=True)
    embed.add_field(name="💵 الرهان",value=f"${bet:,}",           inline=True)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=False)
    add_ach_field(embed, new_ach)
    await msg.edit(content=None, embed=embed)


@bot.command(name="قمار")
async def gamble_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 100 or bet > 50000:
        await ctx.send("❌ الرهان: $100 - $50,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    win = random.random() < 0.5
    if win:
        data["balance"]      += bet
        data["total_earned"] += bet
        data["wins"] += 1
        embed = emb("🃏 قمار — فزت!", f"🎉 ربحت **${bet*2:,}**!", C_GREEN, image_key="gamble")
    else:
        data["balance"]    -= bet
        data["total_lost"] += bet
        data["losses"] += 1
        embed = emb("🃏 قمار — خسرت!", f"😢 خسرت **${bet:,}**!", C_RED, image_key="gamble")

    data["games_played"]  += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)

    embed.add_field(name="💵 الرهان", value=f"${bet:,}",            inline=True)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=True)
    add_ach_field(embed, new_ach)
    await ctx.send(embed=embed)


@bot.command(name="حظ")
async def luck_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 10 or bet > 1000:
        await ctx.send("❌ الرهان: $10 - $1,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    outcomes = [(0, 30), (0.5, 25), (1, 20), (2, 12), (3, 7), (5, 4), (10, 2)]
    mult = random.choices([o[0] for o in outcomes], weights=[o[1] for o in outcomes])[0]
    winnings = int(bet * mult)

    if mult > 1:
        data["balance"]      += winnings - bet
        data["total_earned"] += winnings - bet
        data["wins"] += 1
        color = C_GREEN
        title = f"🍀 حظ سعيد! x{mult}"
        text  = f"🎉 ربحت **${winnings:,}**!"
    elif mult == 1:
        color = C_BLUE
        title = "🍀 حظ عادي!"
        text  = f"😊 استردت **${bet:,}**"
    else:
        data["balance"]    -= bet - winnings
        data["total_lost"] += bet - winnings
        data["losses"] += 1
        color = C_RED
        title = "🍀 حظ سيئ!"
        text  = f"😢 خسرت **${bet - winnings:,}**"

    data["games_played"]  += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)

    embed = emb(title, text, color, image_key="luck")
    embed.add_field(name="💵 الرهان",  value=f"${bet:,}",            inline=True)
    embed.add_field(name="📈 مضاعف",   value=f"x{mult}",              inline=True)
    embed.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}", inline=True)
    add_ach_field(embed, new_ach)
    await ctx.send(embed=embed)
@bot.command(name="دجاجة")
async def chicken_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 50 or bet > 2000:
        await ctx.send("❌ الرهان: $50 - $2,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    multiplier = 1.0
    data["balance"] -= bet

    embed = emb("🐔 لعبة الدجاجة", f"رهانك: **${bet:,}**\nالمضاعف الحالي: **x{multiplier:.2f}**\nاضغط **استمر** أو **اطلع**!", C_ORANGE, image_key="chicken")
    view = discord.ui.View(timeout=60)
    cont_btn = discord.ui.Button(label="🐔 استمر", style=discord.ButtonStyle.primary)
    cash_btn = discord.ui.Button(label="💰 اطلع", style=discord.ButtonStyle.success)
    stopped  = [False]

    async def cont_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
        if stopped[0]: return
        nonlocal multiplier
        if random.random() < 0.35:
            stopped[0] = True
            data["total_lost"]    += bet
            data["losses"]        += 1
            data["games_played"]  += 1
            data["total_gambled"] += bet
            save_db(bot.db)
            e = emb("🐔 الدجاجة ماتت!", f"💀 انتهت اللعبة! خسرت **${bet:,}**\nالمضاعف كان: x{multiplier:.2f}", C_RED, image_key="chicken")
            e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
            await i.response.edit_message(embed=e, view=None)
        else:
            multiplier = round(multiplier + random.uniform(0.2, 0.5), 2)
            e = emb("🐔 لعبة الدجاجة", f"رهانك: **${bet:,}**\nالمضاعف الحالي: **x{multiplier:.2f}**\n\nاضغط **استمر** أو **اطلع**!", C_ORANGE, image_key="chicken")
            await i.response.edit_message(embed=e)

    async def cash_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
        if stopped[0]: return
        stopped[0] = True
        winnings = int(bet * multiplier)
        data["balance"]       += winnings
        data["total_earned"]  += winnings - bet
        data["wins"]          += 1
        data["games_played"]  += 1
        data["total_gambled"] += bet
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb(f"🐔 اطلعت بـ x{multiplier:.2f}!", f"🎉 ربحت **${winnings:,}**!", C_GREEN, image_key="chicken")
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        add_ach_field(e, new_ach)
        await i.response.edit_message(embed=e, view=None)

    cont_btn.callback = cont_cb
    cash_btn.callback = cash_cb
    view.add_item(cont_btn)
    view.add_item(cash_btn)
    await ctx.send(embed=embed, view=view)


@bot.command(name="ألوان")
async def colors_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 50 or bet > 5000:
        await ctx.send("❌ الرهان: $50 - $5,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    colors_list = [("🔴 أحمر", "red"), ("🔵 أزرق", "blue"), ("🟢 أخضر", "green"), ("🟡 أصفر", "yellow")]
    embed  = emb("🎨 لعبة الألوان", f"رهانك: **${bet:,}**\nخمّن اللون الصحيح واربح x2!", C_PURPLE, image_key="colors")
    view   = discord.ui.View()
    chosen = [None]

    for label, value in colors_list:
        btn = discord.ui.Button(label=label, style=discord.ButtonStyle.secondary)
        async def make_cb(v, lbl):
            async def cb(i: discord.Interaction):
                if i.user.id != ctx.author.id:
                    await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
                if chosen[0]: return
                chosen[0] = v
                winning_color = random.choice([c[1] for c in colors_list])
                winning_label = next(l for l, val in colors_list if val == winning_color)
                if v == winning_color:
                    data["balance"]      += bet
                    data["total_earned"] += bet
                    data["wins"] += 1
                    color = C_GREEN
                    title = f"🎨 صح! اخترت {lbl}"
                    text  = f"🎉 ربحت **${bet*2:,}**!"
                else:
                    data["balance"]    -= bet
                    data["total_lost"] += bet
                    data["losses"] += 1
                    color = C_RED
                    title = f"🎨 غلط! كان {winning_label}"
                    text  = f"😢 خسرت **${bet:,}**"
                data["games_played"]  += 1
                data["total_gambled"] += bet
                new_ach = check_achievements(data)
                save_db(bot.db)
                e = emb(title, text, color, image_key="colors")
                e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
                add_ach_field(e, new_ach)
                await i.response.edit_message(embed=e, view=None)
            return cb
        btn.callback = make_cb(value, label)
        view.add_item(btn)
    await ctx.send(embed=embed, view=view)


@bot.command(name="فواكه")
async def fruits_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 50 or bet > 3000:
        await ctx.send("❌ الرهان: $50 - $3,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    fruits = ["🍎","🍊","🍋","🍇","🍓","🍑"]
    row1 = random.choices(fruits, k=3)
    row2 = random.choices(fruits, k=3)
    row3 = random.choices(fruits, k=3)

    matches = sum(1 for r in [row1, row2, row3] if r[0]==r[1]==r[2])
    if matches == 3:
        mult, title = 10, "🍎 ثلاثي مثالي!"
    elif matches == 2:
        mult, title = 5,  "🍎 مزدوج ممتاز!"
    elif matches == 1:
        mult, title = 2,  "🍎 مطابقة واحدة!"
    else:
        mult, title = 0,  "🍎 ما في مطابقة!"

    winnings = bet * mult
    if mult > 0:
        data["balance"]      += winnings - bet
        data["total_earned"] += winnings - bet
        data["wins"] += 1
        color = C_GREEN
    else:
        data["balance"]    -= bet
        data["total_lost"] += bet
        data["losses"] += 1
        color = C_RED

    data["games_played"]  += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)

    embed = emb(title, color=color, image_key="fruits")
    embed.add_field(name="🎰 الصف 1", value=" | ".join(row1), inline=False)
    embed.add_field(name="🎰 الصف 2", value=" | ".join(row2), inline=False)
    embed.add_field(name="🎰 الصف 3", value=" | ".join(row3), inline=False)
    embed.add_field(name="📈 مضاعف",  value=f"x{mult}",        inline=True)
    embed.add_field(name="💰 الأرباح",value=f"${winnings:,}",  inline=True)
    embed.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}", inline=True)
    add_ach_field(embed, new_ach)
    await ctx.send(embed=embed)


@bot.command(name="صناديق")
async def boxes_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 100 or bet > 10000:
        await ctx.send("❌ الرهان: $100 - $10,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    prizes = [
        ("💀 فارغ!",   0,   35),
        ("😐 صغير",   0.5,  25),
        ("😊 عادي",   1.5,  20),
        ("🎉 جيد",    2,    12),
        ("💎 ممتاز",  5,     6),
        ("👑 جاكبوت", 10,    2),
    ]
    embed  = emb("📦 اختر صندوق!", f"رهانك: **${bet:,}**\nاختر صندوقاً من الأربعة!", C_BLUE, image_key="boxes")
    view   = discord.ui.View()
    opened = [False]

    for idx in range(4):
        btn = discord.ui.Button(label=f"📦 صندوق {idx+1}", style=discord.ButtonStyle.primary)
        async def make_cb():
            async def cb(i: discord.Interaction):
                if i.user.id != ctx.author.id:
                    await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
                if opened[0]: return
                opened[0] = True
                prize_label, mult, _ = random.choices(prizes, weights=[p[2] for p in prizes])[0]
                winnings = int(bet * mult)
                if mult > 1:
                    data["balance"]      += winnings - bet
                    data["total_earned"] += winnings - bet
                    data["wins"] += 1
                    color = C_GREEN
                    text  = f"🎉 وجدت {prize_label}! ربحت **${winnings:,}**"
                elif mult > 0:
                    data["balance"]    -= bet - winnings
                    data["total_lost"] += bet - winnings
                    color = C_ORANGE
                    text  = f"{prize_label} استردت **${winnings:,}**"
                else:
                    data["balance"]    -= bet
                    data["total_lost"] += bet
                    data["losses"] += 1
                    color = C_RED
                    text  = f"{prize_label} خسرت **${bet:,}**"
                data["games_played"]  += 1
                data["total_gambled"] += bet
                new_ach = check_achievements(data)
                save_db(bot.db)
                e = emb("📦 فتحت الصندوق!", text, color, image_key="boxes")
                e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
                add_ach_field(e, new_ach)
                await i.response.edit_message(embed=e, view=None)
            return cb
        btn.callback = make_cb()
        view.add_item(btn)
    await ctx.send(embed=embed, view=view)


@bot.command(name="بلاكجاك")
async def blackjack_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 100 or bet > 10000:
        await ctx.send("❌ الرهان: $100 - $10,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    suits = ["♠️","♥️","♦️","♣️"]
    vals  = {"A":11,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}

    def draw(): return (random.choice(list(vals.keys())), random.choice(suits))
    def hand_value(hand):
        v    = sum(vals[c[0]] for c in hand)
        aces = sum(1 for c in hand if c[0]=="A")
        while v > 21 and aces:
            v -= 10; aces -= 1
        return v

    player = [draw(), draw()]
    dealer = [draw(), draw()]

    def render_embed():
        e = emb("🃏 بلاك جاك", f"رهانك: **${bet:,}**", C_GREEN, image_key="blackjack")
        e.add_field(name="يدك",   value=f"{' '.join(c[0]+c[1] for c in player)} = **{hand_value(player)}**", inline=False)
        e.add_field(name="الديلر",value=f"{dealer[0][0]}{dealer[0][1]} ❓", inline=False)
        return e

    view      = discord.ui.View()
    hit_btn   = discord.ui.Button(label="🃏 Hit",   style=discord.ButtonStyle.primary)
    stand_btn = discord.ui.Button(label="🛑 Stand", style=discord.ButtonStyle.danger)

    async def hit_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو دورك!", ephemeral=True); return
        player.append(draw())
        pv = hand_value(player)
        if pv > 21:
            data["balance"]       -= bet
            data["total_lost"]    += bet
            data["losses"]        += 1
            data["games_played"]  += 1
            data["total_gambled"] += bet
            save_db(bot.db)
            e = emb("💥 انفجرت!", f"يدك: {' '.join(c[0]+c[1] for c in player)} = **{pv}**\nخسرت **${bet:,}**", C_RED, image_key="blackjack")
            e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
            await i.response.edit_message(embed=e, view=None)
        else:
            await i.response.edit_message(embed=render_embed())

    async def stand_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو دورك!", ephemeral=True); return
        while hand_value(dealer) < 17:
            dealer.append(draw())
        dv, pv = hand_value(dealer), hand_value(player)
        if dv > 21 or pv > dv:
            data["balance"]      += bet
            data["total_earned"] += bet
            data["wins"] += 1
            text, color = f"🎉 فزت بـ **${bet*2:,}**!", C_GREEN
        elif pv < dv:
            data["balance"]    -= bet
            data["total_lost"] += bet
            data["losses"] += 1
            text, color = f"😢 الديلر فاز! خسرت **${bet:,}**", C_RED
        else:
            text, color = f"🤝 تعادل! استردت **${bet:,}**", C_BLUE
        data["games_played"]  += 1
        data["total_gambled"] += bet
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb(text, "", color, image_key="blackjack")
        e.add_field(name="يدك",   value=f"{' '.join(c[0]+c[1] for c in player)} = **{pv}**", inline=False)
        e.add_field(name="الديلر",value=f"{' '.join(c[0]+c[1] for c in dealer)} = **{dv}**", inline=False)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        add_ach_field(e, new_ach)
        await i.response.edit_message(embed=e, view=None)

    hit_btn.callback   = hit_cb
    stand_btn.callback = stand_cb
    view.add_item(hit_btn)
    view.add_item(stand_btn)
    await ctx.send(embed=render_embed(), view=view)


@bot.command(name="تكس")
async def crash_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 50 or bet > 5000:
        await ctx.send("❌ الرهان: $50 - $5,000!"); return
    if data["balance"] < bet:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")); return

    multiplier  = 1.0
    crash_point = random.uniform(1.1, 10.0)
    cashed_out  = [False]

    def make_embed():
        return emb("📈 تكس", f"رهان: **${bet:,}**\nالمضاعف: **x{multiplier:.2f}**\nاضغط **Cash Out**!", C_ORANGE, image_key="crash")

    view     = discord.ui.View()
    cash_btn = discord.ui.Button(label="💰 Cash Out", style=discord.ButtonStyle.success)

    async def cash_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
        if cashed_out[0]: return
        cashed_out[0] = True
        winnings = int(bet * multiplier)
        data["balance"]       += winnings - bet
        data["total_earned"]  += winnings - bet
        data["wins"]          += 1
        data["games_played"]  += 1
        data["total_gambled"] += bet
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb(f"🎉 Cash Out! x{multiplier:.2f}", f"ربحت **${winnings:,}**", C_GREEN, image_key="crash")
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        add_ach_field(e, new_ach)
        await i.response.edit_message(embed=e, view=None)

    cash_btn.callback = cash_cb
    view.add_item(cash_btn)
    msg = await ctx.send(embed=make_embed(), view=view)

    for _ in range(60):
        await asyncio.sleep(0.5)
        if cashed_out[0]: return
        multiplier += random.uniform(0.05, 0.3)
        multiplier  = round(multiplier, 2)
        if multiplier >= crash_point:
            if not cashed_out[0]:
                cashed_out[0] = True
                data["balance"]       -= bet
                data["total_lost"]    += bet
                data["losses"]        += 1
                data["games_played"]  += 1
                data["total_gambled"] += bet
                save_db(bot.db)
                e = emb(f"💥 انهار عند x{crash_point:.2f}!", f"خسرت **${bet:,}**", C_RED, image_key="crash")
                e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
                await msg.edit(embed=e, view=None)
            return
        if not cashed_out[0]:
            await msg.edit(embed=make_embed())

    if not cashed_out[0]:
        cashed_out[0] = True
        winnings = int(bet * multiplier)
        data["balance"]       += winnings - bet
        data["total_earned"]  += winnings - bet
        data["wins"]          += 1
        data["games_played"]  += 1
        data["total_gambled"] += bet
        save_db(bot.db)
        e = emb(f"🎉 وصلت للحد الأقصى! x{multiplier:.2f}", f"ربحت **${winnings:,}**", C_GREEN, image_key="crash")
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        await msg.edit(embed=e, view=None)
        @bot.command(name="نهب")
async def rob_cmd(ctx, user: discord.User):
    if user.id == ctx.author.id:
        await ctx.send(embed=emb("🤡 يا حبيبي!", get_funny("rob_self"), C_RED, image_key="rob_fail")); return

    data   = get_user(bot.db, str(ctx.author.id))
    victim = get_user(bot.db, str(user.id))

    if victim["balance"] < 500:
        await ctx.send(embed=emb("😂 فقير زيك!", get_funny("rob_poor"), C_RED, image_key="rob_fail")); return

    if victim.get("protection") and victim.get("protection_expires"):
        if datetime.fromisoformat(victim["protection_expires"]) > datetime.now():
            await ctx.send(embed=emb("🛡️ محمي!", "الضحية عندها حماية يونان فاملي! ما تقدر تلمسها!", C_BLUE, image_key="protection"))
            return

    chance = 0.45
    if victim["balance"] > data["balance"] * 2: chance -= 0.15
    if data["properties"].get("cars", 0) > 0:   chance += 0.05

    data["rob_attempts"] += 1
    if random.random() < chance:
        stolen = random.randint(int(victim["balance"] * 0.05), int(victim["balance"] * 0.25))
        victim["balance"]    -= stolen
        data["balance"]      += stolen
        data["total_earned"] += stolen
        data["rob_success"]  += 1
        text    = f"🎉 {get_funny('rob_success')}\n\nسرقت **${stolen:,}** من {user.mention}!"
        color   = C_GREEN
        img_key = "rob"
    else:
        fine = random.randint(500, 2000)
        data["balance"]    -= max(0, fine)
        data["total_lost"] += fine
        data["rob_failed"] += 1
        text    = f"{get_funny('rob_fail')}\n\n❌ تم القبض عليك! دفعت غرامة **${fine:,}**"
        color   = C_RED
        img_key = "rob_fail"

    new_ach = check_achievements(data)
    save_db(bot.db)
    embed = emb("🦹 سرقة", text, color, image_key=img_key)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    add_ach_field(embed, new_ach)
    await ctx.send(embed=embed)


@bot.command(name="حماية")
async def protection_cmd(ctx, hours: int = 24):
    if hours < 1 or hours > 168:
        await ctx.send("❌ المدة: 1 - 168 ساعة!"); return
    data = get_user(bot.db, str(ctx.author.id))
    cost = hours * 500
    if data["balance"] < cost:
        await ctx.send(embed=emb("❌ فلوسك ما تكفي!", f"تكلفة الحماية: ${cost:,}\n{get_funny('broke')}", C_RED, image_key="broke")); return

    data["balance"]           -= cost
    data["protection"]         = True
    data["protection_expires"] = (datetime.now() + timedelta(hours=hours)).isoformat()
    save_db(bot.db)

    embed = emb("🛡️ حماية يونان فاملي!", f"{get_funny('protection_active')}\n\nتم تفعيل الحماية لمدة **{hours} ساعة** مقابل **${cost:,}**", C_BLUE, image_key="protection")
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=True)
    embed.add_field(name="⏰ تنتهي",  value=f"<t:{int((datetime.now()+timedelta(hours=hours)).timestamp())}:R>", inline=True)
    await ctx.send(embed=embed)


@bot.command(name="زواج")
async def marry_cmd(ctx, user: discord.User):
    if user.id == ctx.author.id:
        await ctx.send(embed=emb("🪞 يا نرجسي!", get_funny("marry_self"), C_RED, image_key="marry_self")); return
    if user.bot:
        await ctx.send(embed=emb("🤖 يا حبيبي!", get_funny("marry_bot"), C_RED, image_key="marry_bot")); return

    data    = get_user(bot.db, str(ctx.author.id))
    partner = get_user(bot.db, str(user.id))

    if data["married_to"]:
        await ctx.send(embed=emb("😂 يا حبيبي!", get_funny("already_married"), C_RED, image_key="marry")); return
    if partner["married_to"]:
        await ctx.send(embed=emb("💔 للأسف!", get_funny("partner_married"), C_RED, image_key="marry")); return

    embed  = emb("💍 عرض زواج يوناني!", f"{ctx.author.mention} يعرض الزواج على {user.mention}!\nالمهر: **$5,000** 💎", C_PINK, image_key="marry")
    view   = discord.ui.View()
    yes_btn= discord.ui.Button(label="💍 نعم!", style=discord.ButtonStyle.success)
    no_btn = discord.ui.Button(label="❌ لا",   style=discord.ButtonStyle.danger)

    async def yes_cb(i: discord.Interaction):
        if i.user.id != user.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        if data["balance"] < 5000:
            await i.response.send_message("❌ فلوسك ما تكفي للمهر!", ephemeral=True); return
        data["balance"]       -= 5000
        partner["balance"]    += 5000
        data["married_to"]     = str(user.id)
        partner["married_to"]  = str(ctx.author.id)
        data["married_since"]  = partner["married_since"] = datetime.now().isoformat()
        data["dowry"]          = partner["dowry"] = 5000
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb("💍 زواج يوناني ناجح!", f"{ctx.author.mention} ❤️ {user.mention}\nمبروك يا عروسين! 🎉", C_PINK, image_key="marry")
        add_ach_field(e, new_ach)
        await i.response.edit_message(embed=e, view=None)

    async def no_cb(i: discord.Interaction):
        if i.user.id != user.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        e = emb("💔 رفض يوناني!", f"{user.mention} رفض عرض {ctx.author.mention}!", C_RED, image_key="divorce")
        await i.response.edit_message(embed=e, view=None)

    yes_btn.callback = yes_cb
    no_btn.callback  = no_cb
    view.add_item(yes_btn)
    view.add_item(no_btn)
    await ctx.send(embed=embed, view=view)


@bot.command(name="طلاق")
async def divorce_cmd(ctx):
    data = get_user(bot.db, str(ctx.author.id))
    if not data["married_to"]:
        await ctx.send(embed=emb("🤣 يا حبيبي!", get_funny("not_married"), C_RED, image_key="divorce")); return

    if data.get("last_divorce"):
        if datetime.now() - datetime.fromisoformat(data["last_divorce"]) < timedelta(hours=24):
            await ctx.send(embed=emb("⏳ انتظر!", get_funny("divorce_cooldown"), C_RED, image_key="divorce")); return

    partner_id = data["married_to"]
    partner    = get_user(bot.db, partner_id)

    embed  = emb("💔 طلاق يوناني", f"متأكد تبي تطلق؟\nراح تخسر نصف مهرك (${data['dowry']//2:,}) 💸", C_RED, image_key="divorce")
    view   = discord.ui.View()
    yes_btn= discord.ui.Button(label="💔 نعم، طلق", style=discord.ButtonStyle.danger)
    no_btn = discord.ui.Button(label="❌ إلغاء",     style=discord.ButtonStyle.secondary)

    async def yes_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        loss = data["dowry"] // 2
        data["balance"]       -= max(0, loss)
        partner["balance"]    += loss
        data["divorce_count"] += 1
        data["last_divorce"]   = datetime.now().isoformat()
        data["married_to"]     = partner["married_to"]   = None
        data["married_since"]  = partner["married_since"] = None
        save_db(bot.db)
        e = emb("💔 تم الطلاق!", f"{ctx.author.mention} طلّق!\nخسر **${loss:,}** 💸", C_RED, image_key="divorce")
        await i.response.edit_message(embed=e, view=None)

    async def no_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        await i.response.edit_message(embed=emb("✅ إلغاء الطلاق", "تراجعت! يونان فاملي يحب الاستقرار 💕", C_GREEN), view=None)

    yes_btn.callback = yes_cb
    no_btn.callback  = no_cb
    view.add_item(yes_btn)
    view.add_item(no_btn)
    await ctx.send(embed=embed, view=view)


@bot.command(name="ممتلكات")
async def properties_cmd(ctx):
    data  = get_user(bot.db, str(ctx.author.id))
    embed = emb("🏢 ممتلكات يونان فاملي", "استثمر وأربح دخل سلبي! 💼", C_GOLD, image_key="properties")
    for key, prop in PROPERTIES.items():
        owned = data["properties"].get(key, 0)
        embed.add_field(
            name=f"{prop['icon']} {prop['name']} (تمتلك: {owned})",
            value=f"السعر: **${prop['price']:,}**\nالدخل: **${prop['income']:,}/يوم**\n{prop['desc']}",
            inline=True,
        )

    view = discord.ui.View()
    # تصحيح: عرض كل الممتلكات (Discord يقبل 5 أزرار فقط في صف، نأخذ الـ 5 الأرخص)
    affordable = sorted(PROPERTIES.items(), key=lambda x: x[1]["price"])[:5]
    for key, prop in affordable:
        btn = discord.ui.Button(label=f"شراء {prop['name']}", emoji=prop["icon"], style=discord.ButtonStyle.primary)

        async def make_cb(k, p):
            async def cb(i: discord.Interaction):
                if i.user.id != ctx.author.id:
                    await i.response.send_message("❌ مو لك!", ephemeral=True); return
                d = get_user(bot.db, str(i.user.id))
                if d["balance"] < p["price"]:
                    await i.response.send_message(embed=emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED), ephemeral=True); return
                d["balance"]       -= p["price"]
                d["properties"][k]  = d["properties"].get(k, 0) + 1
                new_ach = check_achievements(d)
                save_db(bot.db)
                e = emb(f"✅ اشتريت {p['name']}!", f"{get_funny('buy_property')}\n\nرصيدك: ${d['balance']:,}", C_GREEN, image_key="properties")
                add_ach_field(e, new_ach)
                await i.response.send_message(embed=e, ephemeral=True)
            return cb

        btn.callback = make_cb(key, prop)
        view.add_item(btn)
    await ctx.send(embed=embed, view=view)
    @bot.command(name="مستوى")
async def level_cmd(ctx, user: Optional[discord.User] = None):
    target     = user or ctx.author
    data       = get_user(bot.db, str(target.id))
    xp_needed  = data["level"] * 1000
    xp_progress= data["xp"] % xp_needed if xp_needed else 0
    embed = emb(f"⚡ مستوى — {target.display_name}", f"**{get_rank(data['level'])}** | مستوى {data['level']}", C_PURPLE, image_key="level_up")
    bar   = progress_bar(xp_progress, xp_needed, 20)
    pct   = f"{xp_progress/xp_needed*100:.1f}%" if xp_needed else "0%"
    embed.add_field(name="📊 التقدم", value=f"`{bar}` {pct}\n{xp_progress:,} / {xp_needed:,} XP", inline=False)
    embed.add_field(name="🎮 ألعاب",  value=f"{data['games_played']}", inline=True)
    embed.add_field(name="🏆 فوز",    value=f"{data['wins']}",         inline=True)
    embed.add_field(name="💀 خسارة",  value=f"{data['losses']}",       inline=True)
    await ctx.send(embed=embed)


@bot.command(name="مساعدة")
async def help_cmd(ctx):
    embed = emb("📖 دليل YF BANK — عائلة يونان", "أقوى بوت اقتصادي في ديسكورد! 💎", C_GOLD, image_key="help")
    cmds = [
        ("💳 -رصيد",      "عرض رصيدك وممتلكاتك"),
        ("🎁 -يومي",      "المكافأة اليومية"),
        ("🏆 -مطنوخين",   "قائمة أغنى الأعضاء"),
        ("📊 -سوق",       "سوق الموارد الحي"),
        ("🛒 -شراء",      "شراء من السوق"),
        ("💰 -بيع",       "بيع في السوق"),
        ("🎮 -ألعاب",     "قائمة الألعاب"),
        ("🎰 -سلات",      "آلة الحظ ($50-$5K)"),
        ("🎡 -عجلة",      "عجلة الحظ ($100-$50K)"),
        ("🎲 -نرد",       "لعبة النرد ($100-$10K)"),
        ("🃏 -قمار",      "50/50 ($100-$50K)"),
        ("🍀 -حظ",        "جرب حظك ($10-$1K)"),
        ("🐔 -دجاجة",     "الدجاجة الجريئة ($50-$2K)"),
        ("🎨 -ألوان",     "خمّن اللون ($50-$5K)"),
        ("🍎 -فواكه",     "مطابقة الفواكه ($50-$3K)"),
        ("📦 -صناديق",    "افتح الصندوق ($100-$10K)"),
        ("🃏 -بلاكجاك",  "بلاك جاك 21 ($100-$10K)"),
        ("📈 -تكس",       "تكس — اطلع قبل الانهيار"),
        ("🦹 -نهب",       "سرق مستخدم"),
        ("🛡️ -حماية",    "اشتري حماية من السرقة"),
        ("💍 -زواج",      "تزوج مستخدم"),
        ("💔 -طلاق",      "طلق شريكك"),
        ("🏢 -ممتلكات",   "اشترِ ممتلكات"),
        ("💸 -تحويل",     "حول فلوس لشخص"),
        ("🏛️ -إيداع",    "إيداع في البنك"),
        ("🏛️ -سحب",      "سحب من البنك"),
        ("⚡ -مستوى",     "عرض مستواك"),
    ]
    for name, desc in cmds:
        embed.add_field(name=name, value=desc, inline=True)
    embed.add_field(name="💡 نصيحة يونانية", value="استخدم `-يومي` كل يوم وبني سلسلة للمكافآت الإضافية! 🔥", inline=False)
    await ctx.send(embed=embed)


@bot.command(name="ابدأ")
async def start_cmd(ctx):
    embed = emb("🏦 YF BANK — قائمة الأوامر", "عائلة يونان ترحب بك! 👑", C_GOLD, image_key="commands")
    embed.add_field(name="🎮 الألعاب",    value="سلات، عجلة، نرد، دجاجة، فواكه، ألوان، صناديق، قمار، بلاكجاك، تكس، حظ", inline=False)
    embed.add_field(name="💰 المال",      value="رصيد، يومي، إيداع، سحب، تحويل", inline=False)
    embed.add_field(name="📊 التداول",    value="سوق، شراء، بيع، ممتلكات",       inline=False)
    embed.add_field(name="👤 الحسابات",   value="رصيد، مطنوخين، مستوى",           inline=False)
    embed.add_field(name="🔒 الأمان",     value="نهب، حماية",                     inline=False)
    embed.add_field(name="💍 الاجتماعية", value="زواج، طلاق",                     inline=False)
    await ctx.send(embed=embed)


@bot.event
async def on_ready():
    print(f"✅ YF BANK Online! {bot.user.name} ({bot.user.id})")
    print("عائلة يونان — أقوى بوت اقتصادي في ديسكورد!")
    print(f"الأوامر المتوفرة: {len(bot.commands)}")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="عائلة يونان | -ابدأ"),
        status=discord.Status.online
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=emb("❓ أمر غير معروف!", "استخدم `-مساعدة` لعرض قائمة الأوامر\nأو `-ابدأ` للبدء 🎮", C_RED, image_key="help"))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=emb("⚠️ ناقص معلومات!", "استخدم الأمر بشكل صحيح\nاكتب `-مساعدة` للمساعدة", C_ORANGE, image_key="help"))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=emb("⚠️ خطأ في المدخلات!", "تأكد من إدخال الأرقام بشكل صحيح", C_ORANGE, image_key="help"))
    else:
        print(f"Error: {error}")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
