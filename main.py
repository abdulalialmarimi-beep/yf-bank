"""
╔══════════════════════════════════════════════════════════════════╗
║  YF BANK - Yonan Family Discord Economy Bot                     ║
║  أقوى بوت اقتصادي في تاريخ ديسكورد - عائلة يونان               ║
║  النسخة المطورة - كل الأوامر بالعربية مع صور وفكاهة             ║
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

# ═══════════════════════════════════════════════════════════════════
# إعدادات البوت
# ═══════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════
# إعدادات Replit - استخدم Secrets للتوكن
# ═══════════════════════════════════════════════════════════════════
# 1. اضغط على "Tools" → "Secrets" في Replit
# 2. أضف Secret جديد:
#    Key: DISCORD_TOKEN
#    Value: توكن_البوت_الحقيقي
# ═══════════════════════════════════════════════════════════════════

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
if not BOT_TOKEN:
    print("❌ خطأ: ما في توكن!")
    print("📝 روح لـ Tools → Secrets في Replit")
    print("🔑 أضف: DISCORD_TOKEN = توكن_البوت")
    exit(1)
COMMAND_PREFIX = "-"

C_GOLD = 0xd4a843
C_GREEN = 0x4ade80
C_RED = 0xf87171
C_BLUE = 0x60a5fa
C_PINK = 0xff69b4
C_PURPLE = 0x9333ea
C_ORANGE = 0xf97316
C_CYAN = 0x22d3ee
C_DARK = 0x1a1a2e

DB_FILE = "yf_bank_data.json"

# ═══════════════════════════════════════════════════════════════════
# مسار الصور المحلية - رفعها على Discord/Imgur واستبدل الروابط
# ═══════════════════════════════════════════════════════════════════
# ملاحظة: الصور المحلية ما تشتغل في Discord Embed
# لازم ترفعها على Discord أو Imgur وتحط الروابط المباشرة
# 
# كيف ترفع على Discord:
# 1. ارسل الصورة في أي قناة
# 2. اضغط يمين → "Copy Link" 
# 3. استبدل الرابط هنا
#
# كيف ترفع على Imgur:
# 1. روح imgur.com/upload
# 2. ارفع الصورة
# 3. خذ الرابط المباشر (ينتهي بـ .png)

IMAGES = {
    # الصور الرئيسية
    "logo": "https://cdn.discordapp.com/attachments/.../logo.png",       # ← استبدل
    "bank": "https://cdn.discordapp.com/attachments/.../bank.png",       # ← استبدل

    # الصور المالية
    "balance": "https://cdn.discordapp.com/attachments/.../balance.png",   # ← استبدل
    "daily": "https://cdn.discordapp.com/attachments/.../daily.png",     # ← استبدل
    "top": "https://cdn.discordapp.com/attachments/.../top.png",         # ← استبدل
    "broke": "https://cdn.discordapp.com/attachments/.../broke.png",     # ← استبدل
    "transfer": "https://cdn.discordapp.com/attachments/.../transfer.png", # ← استبدل

    # السوق والتداول
    "market": "https://cdn.discordapp.com/attachments/.../market.png",   # ← استبدل
    "properties": "https://cdn.discordapp.com/attachments/.../properties.png", # ← استبدل

    # الألعاب
    "games": "https://cdn.discordapp.com/attachments/.../games.png",   # ← استبدل
    "slots": "https://cdn.discordapp.com/attachments/.../slots.png",   # ← استبدل
    "wheel": "https://cdn.discordapp.com/attachments/.../wheel.png",   # ← استبدل
    "blackjack": "https://cdn.discordapp.com/attachments/.../blackjack.png", # ← استبدل
    "crash": "https://cdn.discordapp.com/attachments/.../crash.png",   # ← استبدل
    "dice": "https://cdn.discordapp.com/attachments/.../dice.png",     # ← استبدل
    "chicken": "https://cdn.discordapp.com/attachments/.../chicken.png", # ← استبدل
    "colors": "https://cdn.discordapp.com/attachments/.../colors.png", # ← استبدل
    "fruits": "https://cdn.discordapp.com/attachments/.../fruits.png", # ← استبدل
    "boxes": "https://cdn.discordapp.com/attachments/.../boxes.png",   # ← استبدل
    "gamble": "https://cdn.discordapp.com/attachments/.../gamble.png", # ← استبدل
    "luck": "https://cdn.discordapp.com/attachments/.../luck.png",     # ← استبدل

    # التفاعل الاجتماعي
    "marry": "https://cdn.discordapp.com/attachments/.../marry.png",   # ← استبدل
    "divorce": "https://cdn.discordapp.com/attachments/.../divorce.png", # ← استبدل
    "marry_bot": "https://cdn.discordapp.com/attachments/.../marry_bot.png", # ← استبدل
    "marry_self": "https://cdn.discordapp.com/attachments/.../marry_self.png", # ← استبدل

    # النهب والحماية
    "rob": "https://cdn.discordapp.com/attachments/.../rob.png",     # ← استبدل
    "rob_fail": "https://cdn.discordapp.com/attachments/.../rob_fail.png", # ← استبدل
    "protection": "https://cdn.discordapp.com/attachments/.../protection.png", # ← استبدل

    # المساعدة
    "help": "https://cdn.discordapp.com/attachments/.../help.png",     # ← استبدل
    "commands": "https://cdn.discordapp.com/attachments/.../commands.png", # ← استبدل

    # الإنجازات
    "achievement": "https://cdn.discordapp.com/attachments/.../achievement.png", # ← استبدل
    "jackpot": "https://cdn.discordapp.com/attachments/.../jackpot.png", # ← استبدل
    "level_up": "https://cdn.discordapp.com/attachments/.../level_up.png", # ← استبدل
}

# ═══════════════════════════════════════════════════════════════════
# رسائل فكاهية عائلة يونان
# ═══════════════════════════════════════════════════════════════════

FUNNY_MESSAGES = {
    "broke": [
        "يا اخي حتى الفقر ما يجي فخامة زيك! محفظتك صارت تعيش في خيمة!",
        "يونان فاملي ما يعرف الفقر! بس انت واضح انك عضو شرفي في نادي الفقراء!",
        "حتى الريال يونان يبكي لما يشوف رصيدك! روح اشتغل شوي يا بطل!",
        "رصيدك صفر؟ حتى المهرجين في السيرك عندهم فلوس اكثر منك!",
        "يا ولد حتى الجثة في القبر عندها اكثر من رصيدك!",
    ],
    "marry_bot": [
        "يا حبيبي تبي تتزوج بوت؟ وش نوع العلاقة هذي؟ رومانسية رقمية؟",
        "يونان فاملي يدعم الحب بكل اشكاله! بس البوت ما يقدر يوقع عقد زواج يا ذكي!",
        "البوت قال لي: انا ما ابي اتزوج انسان بطيء المعالجة!",
        "تبي تتزوج بوت؟ روح دور لك بوت ثاني يقبلك، هذا مشغول!",
    ],
    "marry_self": [
        "تبي تتزوج نفسك؟ حتى المراة تستحي منك يا نرجسي!",
        "يونان فاملي يحب الثقة بالنفس! بس كذا زيادة يا بطل!",
        "حتى نفسك ما تبي تتزوجك! فكر فيها شوي!",
        "يا اخي روح دور لك حبيب، ما في احد يتزوج نفسه غيرك!",
    ],
    "rob_self": [
        "تبي تسرق نفسك؟ يونان فاملي ما يقبل الغباء بس انت تستاهل جائزة!",
        "سرقت نفسك؟ كيف؟ مسكت ايدك اليمين بايدك اليسار؟",
        "يا ذكي! روح سرق غيرك، نفسك ما عندها فلوس اصلا!",
    ],
    "rob_poor": [
        "تبي تسرق فقير؟ حتى اللصوص في يونان فاملي عندهم اخلاق!",
        "سرقت فقير؟ يعطيك العافية! سرقت منه... الهواء؟",
        "الضحية فقير زيك! روحوا افتحوا نادي الفقراء مع بعض!",
    ],
    "transfer_self": [
        "تحول لنفسك؟ يونان فاملي يحب الذكاء! بس انت زيادة!",
        "حولت لنفسك؟ كانك تعطي نفسك هدية في عيد ميلادك!",
        "يا بطل! الفلوس راحت وجت... لنفس المحفظة!",
    ],
    "divorce_cooldown": [
        "يا ولد كم مرة تبي تطلق؟ يونان فاملي مش محكمة استئناف!",
        "صارلك ساعة متزوج وبتطلق؟ حتى الستين ما تطلق بسرعتك!",
        "روح استقر شوي! يونان فاملي يحب الاستقرار العائلي!",
    ],
    "already_married": [
        "يا حبيبي انت متزوج! وش تبي؟ زوجة ثانية؟ يونان فاملي مو مسلسل تركي!",
        "عندك زوج! روح اهتم فيها بدل ما تدور على ثانية!",
        "تبي تتزوج وانت متزوج؟ حتى سلمان خان ما يقدر!",
    ],
    "partner_married": [
        "الشخص متزوج! تبي تخرب بيته؟ يونان فاملي ما يقبل الخيانة!",
        "روح دور لك عزابي! ما في داعي تسرق زوج غيرك!",
    ],
    "not_married": [
        "انت مو متزوج! وش بتطلق؟ نفسك؟",
        "تبي تطلق وانت عازب؟ يونان فاملي يحب الاحلام بس كذا زيادة!",
    ],
    "rob_fail": [
        "الشرطة قبضت عليك! يونان فاملي ما يحمي اللصوص الفاشلين!",
        "مسكتك الشرطة! حتى في السرقة انت فاشل!",
        "انكشفت! روح اشتغل شريف افضل لك!",
    ],
    "rob_success": [
        "يونان فاملي يفتخر بك! لص محترف وبارع!",
        "سرقة ناجحة! يونان فاملي يعلم فنون السرقة من جيل لجيل!",
        "مسكتها! يونان فاملي يسلم عليك يا لص المحترفين!",
    ],
    "daily_streak": [
        "يا سلام! سلسلة يونان فاملي قوية! {streak} ايام!",
        "مستمر يا بطل! عائلة يونان فخورة فيك!",
        "ما شاء الله! ثبات يوناني اصيل!",
    ],
    "level_up": [
        "يونان فاملي تهنئك! وصلت لمستوى جديد!",
        "تطورت يا اسطورة! يونان فاملي تفتخر فيك!",
        "صاروخ يونان فاملي! مستوى جديد!",
    ],
    "jackpot": [
        "يا ولد! جاكبوت يونان فاملي! انت مليونير الان!",
        "يونان فاملي تبارك لك! فزت بالجاكبوت الاسطوري!",
        "صرت غني! يونان فاملي تبغى قرض منك!",
    ],
    "protection_active": [
        "عندك حماية يونان فاملي! ما حد يقدر يلمسك!",
        "يونان فاملي يحميك! الشرطة على اهبة الاستعداد!",
    ],
    "buy_property": [
        "صار عندك عقار! يونان فاملي تصير رجل اعمال!",
        "استثمار ذكي! يونان فاملي تفتخر فيك!",
    ],
}

# ═══════════════════════════════════════════════════════════════════
# قاعدة البيانات
# ═══════════════════════════════════════════════════════════════════

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
                "cars": 0, "stocks": 0, "lands": 0, "trains": 0,
                "phones": 0, "companies": 0, "servers": 0, "diamonds": 0,
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
    "bitcoin": {"name": "بيتكوين", "icon": "\u20BF", "buy": 49000, "sell": 44000},
    "gold": {"name": "ذهب", "icon": "\U0001F947", "buy": 5000, "sell": 4500},
    "diamond": {"name": "الماس", "icon": "\U0001F48E", "buy": 8200, "sell": 7400},
    "silver": {"name": "فضة", "icon": "\U0001F948", "buy": 986, "sell": 887},
    "emerald": {"name": "زمرد", "icon": "\U0001F49A", "buy": 5900, "sell": 5300},
    "ruby": {"name": "ياقوت", "icon": "\u2764\uFE0F", "buy": 6300, "sell": 5700},
    "platinum": {"name": "بلاتين", "icon": "\u26AA", "buy": 15000, "sell": 13500},
    "oil": {"name": "نفط", "icon": "\U0001F6E2\uFE0F", "buy": 8000, "sell": 7200},
}

PROPERTIES = {
    "cars": {"name": "سيارات", "icon": "\U0001F697", "price": 50000, "income": 5000, "desc": "تاجير سيارات فاخرة"},
    "stocks": {"name": "اسهم", "icon": "\U0001F4CA", "price": 10000, "income": 1000, "desc": "محفظة استثمارية"},
    "lands": {"name": "اراضي", "icon": "\U0001F3D9\uFE0F", "price": 100000, "income": 8000, "desc": "عقارات وتطوير"},
    "trains": {"name": "قطارات", "icon": "\U0001F682", "price": 200000, "income": 15000, "desc": "خطوط نقل"},
    "phones": {"name": "هواتف", "icon": "\U0001F4F1", "price": 5000, "income": 500, "desc": "محل الكترونيات"},
    "companies": {"name": "شركات", "icon": "\U0001F4BB", "price": 500000, "income": 30000, "desc": "امبراطورية اعمال"},
    "servers": {"name": "سيرفرات", "icon": "\U0001F5A5\uFE0F", "price": 20000, "income": 2000, "desc": "استضافة سحابية"},
    "diamonds": {"name": "الماس", "icon": "\U0001F48E", "price": 50000, "income": 4000, "desc": "مناجم الماس"},
}

GAMES = {
    "slots": {"name": "سلات", "icon": "\U0001F3B0", "desc": "جاكبوت 50K!", "min": 50, "max": 5000, "color": C_GOLD, "image": "slots"},
    "dice": {"name": "نرد", "icon": "\U0001F3B2", "desc": "الاعلى رقم يفوز", "min": 100, "max": 10000, "color": C_BLUE, "image": "dice"},
    "chicken": {"name": "دجاجة", "icon": "\U0001F414", "desc": "كم تقدر تستمر؟", "min": 50, "max": 2000, "color": C_ORANGE, "image": "chicken"},
    "colors": {"name": "الوان", "icon": "\U0001F3A8", "desc": "خمن اللون x2", "min": 50, "max": 5000, "color": C_PURPLE, "image": "colors"},
    "fruits": {"name": "فواكه", "icon": "\U0001F34E", "desc": "مطابقة الفواكه حتى x10", "min": 50, "max": 3000, "color": C_GREEN, "image": "fruits"},
    "boxes": {"name": "صناديق", "icon": "\U0001F4E6", "desc": "افتح الصندوق!", "min": 100, "max": 10000, "color": C_BLUE, "image": "boxes"},
    "wheel": {"name": "عجلة", "icon": "\U0001F3A1", "desc": "دور العجلة حتى x10", "min": 100, "max": 50000, "color": C_PINK, "image": "wheel"},
    "gamble": {"name": "قمار", "icon": "\U0001F0CF", "desc": "50/50 كل شيء او لا شيء", "min": 100, "max": 50000, "color": C_RED, "image": "gamble"},
    "blackjack": {"name": "بلاك جاك", "icon": "\U0001F0CF", "desc": "21 نقطة", "min": 100, "max": 10000, "color": C_GREEN, "image": "blackjack"},
    "crash": {"name": "تكس", "icon": "\U0001F4C8", "desc": "اطلع قبل ما ينهار!", "min": 50, "max": 5000, "color": C_ORANGE, "image": "crash"},
    "luck": {"name": "حظ", "icon": "\U0001F340", "desc": "جرب حظك حتى x10", "min": 10, "max": 1000, "color": C_GREEN, "image": "luck"},
}

ACHIEVEMENTS = {
    "first_win": {"name": "اول فوز", "desc": "اربح لعبتك الاولى", "reward": 100},
    "rich": {"name": "غني", "desc": "وصل لـ 100,000", "reward": 5000},
    "millionaire": {"name": "مليونير", "desc": "وصل لـ 1,000,000", "reward": 50000},
    "jackpot": {"name": "جاكبوت", "desc": "اربح الجاكبوت في السلات", "reward": 10000},
    "married": {"name": "متزوج", "desc": "تزوج بنجاح", "reward": 1000},
    "robber": {"name": "لص محترف", "desc": "نجح في 10 سرقات", "reward": 5000},
    "streak_7": {"name": "متسلسل", "desc": "سلسلة 7 ايام", "reward": 2000},
    "streak_30": {"name": "اسطوري", "desc": "سلسلة 30 يوم", "reward": 20000},
    "level_10": {"name": "نجم", "desc": "وصل للمستوى 10", "reward": 5000},
    "level_50": {"name": "اله", "desc": "وصل للمستوى 50", "reward": 100000},
    "properties_10": {"name": "مستثمر", "desc": "اشترِ 10 ممتلكات", "reward": 10000},
    "games_100": {"name": "لاعب محترف", "desc": "العب 100 لعبة", "reward": 5000},
}

# ═══════════════════════════════════════════════════════════════════
# إعدادات البوت
# ═══════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════
# دوال مساعدة
# ═══════════════════════════════════════════════════════════════════

def emb(title, desc="", color=C_GOLD, image_key=None, thumbnail_key=None):
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now())
    e.set_footer(text="YF BANK 2026 | عائلة يونان", icon_url=IMAGES.get("logo"))
    if image_key and image_key in IMAGES:
        e.set_image(url=IMAGES[image_key])
    if thumbnail_key and thumbnail_key in IMAGES:
        e.set_thumbnail(url=IMAGES[thumbnail_key])
    return e


def get_rank(lvl):
    ranks = ["مبتدئ", "تاجر", "مستثمر", "مليونير", "اسطورة", "اله يوناني"]
    return ranks[min(lvl // 10, 5)]


def progress_bar(current, total, length=15):
    filled = int(length * current / total)
    return "█" * filled + "░" * (length - filled)


def format_money(amount):
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"{amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"{amount / 1_000:.1f}K"
    return str(amount)


def get_funny(key, **kwargs):
    msgs = FUNNY_MESSAGES.get(key, ["🤔"])
    msg = random.choice(msgs)
    return msg.format(**kwargs)


def check_achievements(data):
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

# ═══════════════════════════════════════════════════════════════════
# الأوامر بالعربية
# ═══════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────
# رصيد
# ───────────────────────────────────────────
@bot.command(name="رصيد")
async def balance_cmd(ctx, user: Optional[discord.User] = None):
    target = user or ctx.author
    data = get_user(bot.db, str(target.id))
    total = data["balance"] + data["bank"]
    xp_needed = data["level"] * 1000
    xp_progress = data["xp"] % xp_needed
    data["last_active"] = datetime.now().isoformat()
    save_db(bot.db)

    funny_note = ""
    if total < 1000:
        funny_note = f"\n\n{get_funny('broke')}"

    embed = emb(
        f"محفظة — {target.display_name} {'👑' if data['level'] >= 30 else ''}",
        f"## 💰 ${format_money(total)}\nالرصيد الكلي • عملات YF{funny_note}",
        C_GOLD,
        image_key="balance"
    )

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
    view.add_item(discord.ui.Button(
        view.add_item(discord.ui.Button(label="🏛️ إيداع", style=discord.ButtonStyle.success))
    view.add_item(discord.ui.Button(label="📊 تداول", style=discord.ButtonStyle.secondary))

    await ctx.send(embed=embed, view=view)


# ───────────────────────────────────────────
# يومي
# ───────────────────────────────────────────
@bot.command(name="يومي")
async def daily_cmd(ctx):
    data = get_user(bot.db, str(ctx.author.id))
    now = datetime.now()
    if data["last_daily"]:
        last = datetime.fromisoformat(data["last_daily"])
        diff = now - last
        if diff < timedelta(hours=24):
            remaining = timedelta(hours=24) - diff
            h = int(remaining.total_seconds() // 3600)
            m = int((remaining.total_seconds() % 3600) // 60)
            embed = emb(
                "⏳ المكافأة اليومية",
                f"{get_funny('broke')}\n\nارجع بعد **{h}س {m}د** ⏰",
                C_RED,
                image_key="broke"
            )
            await ctx.send(embed=embed)
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

    streak_msg = get_funny("daily_streak", streak=data["streak"]) if data["streak"] > 1 else ""

    embed = emb("🎁 تم استلام المكافأة!", color=C_GREEN, image_key="daily")
    embed.add_field(name="💰 أساسية", value=f"${base:,}", inline=True)
    embed.add_field(name="🔥 سلسلة", value=f"${streak_bonus:,} (x{data['streak']})", inline=True)
    embed.add_field(name="⚡ مستوى", value=f"${level_bonus:,}", inline=True)
    embed.add_field(name="💎 إجمالي", value=f"**${total:,}**", inline=False)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=True)
    embed.add_field(name="🔥 سلسلة", value=f"**{data['streak']} أيام**", inline=True)
    if streak_msg:
        embed.add_field(name="🎉 يونان فاملي تقول:", value=streak_msg, inline=False)
    if new_ach:
        embed.add_field(
            name="🏆 إنجاز جديد!",
            value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            inline=False,
        )
    await ctx.send(embed=embed)


# ───────────────────────────────────────────
# مطنوخين (توب)
# ───────────────────────────────────────────
@bot.command(name="مطنوخين")
async def top_cmd(ctx):
    embed = emb("🏆 قائمة المطنوخين — عائلة يونان", "أغنى وأقوى أعضاء العائلة! 💎", C_GOLD, image_key="top")
    users_data = [
        (m, d["balance"] + d["bank"], d["level"])
        for uid, d in bot.db.items()
        if (m := ctx.guild.get_member(int(uid)))
    ]
    users_data.sort(key=lambda x: x[1], reverse=True)
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for i, (member, total, lvl) in enumerate(users_data[:10]):
        rank_emoji = "👑" if i == 0 else "💎" if i == 1 else "🥉" if i == 2 else "🌟"
        embed.add_field(
            name=f"{medals[i] if i < 3 else f'#{i+1}'} {rank_emoji} {member.display_name}",
            value=f"💰 ${format_money(total)} | ⚡ Lvl {lvl} | {get_rank(lvl)}",
            inline=False,
        )

    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="💰 الأغنى", style=discord.ButtonStyle.primary))
    view.add_item(discord.ui.Button(label="📈 المستوى", style=discord.ButtonStyle.secondary))
    view.add_item(discord.ui.Button(label="💀 اللصوص", style=discord.ButtonStyle.danger))
    await ctx.send(embed=embed, view=view)


# ───────────────────────────────────────────
# سوق
# ───────────────────────────────────────────
@bot.command(name="سوق")
async def market_cmd(ctx):
    embed = emb("📊 سوق YF — الأسعار الحية", "تتغير كل 30 دقيقة | عائلة يونان للتداول 💹", C_GOLD, image_key="market")
    for key, item in bot.market.items():
        original = MARKET[key]["buy"]
        change = ((item["buy"] - original) / original) * 100
        emoji = "🟢📈" if change >= 0 else "🔴📉"
        embed.add_field(
            name=f"{item['icon']} {item['name']}",
            value=f"{emoji} شراء: `${format_money(item['buy'])}`\nبيع: `${format_money(item['sell'])}`\nتغير: `{change:+.2f}%`",
            inline=True,
        )
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="🛒 شراء", style=discord.ButtonStyle.success))
    view.add_item(discord.ui.Button(label="💰 بيع", style=discord.ButtonStyle.danger))
    view.add_item(discord.ui.Button(label="📦 مخزن", style=discord.ButtonStyle.secondary))
    await ctx.send(embed=embed, view=view)


# ───────────────────────────────────────────
# ألعاب
# ───────────────────────────────────────────
@bot.command(name="ألعاب")
async def games_cmd(ctx):
    embed = emb("🎮 ألعاب يونان فاملي", "💎 💎 💎 جاكبوت! +$50,000 ✨\nاختر لعبتك يا بطل!", C_GOLD, image_key="games")
        embed = emb("🎮 ألعاب يونان فاملي", "💎 💎 💎 جاكبوت! +$50,000 ✨\nاختر لعبتك يا بطل!", C_GOLD, image_key="games")
    for key, game in GAMES.items():
        embed.add_field(
            name=f"{game['icon']} {game['name']}",
            value=f"{game['desc']}\nحد: `${game['min']:,}-${game['max']:,}`",
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
        e = emb(f"{g['icon']} {g['name']}", f"{g['desc']}\nحد الرهان: `${g['min']:,}-${g['max']:,}`", g["color"], image_key=g.get("image"))
        v = discord.ui.View()
        for amt in [100, 500, 1000, 5000]:
            if g["min"] <= amt <= g["max"]:
                v.add_item(discord.ui.Button(label=f"لعب ${amt:,}", style=discord.ButtonStyle.primary))
        v.add_item(discord.ui.Button(label="💰 كل شيء", style=discord.ButtonStyle.danger))
        await i.response.send_message(embed=e, view=v)

    select.callback = cb
    view = discord.ui.View()
    view.add_item(select)
    await ctx.send(embed=embed, view=view)

# ───────────────────────────────────────────
# سلات
# ───────────────────────────────────────────
@bot.command(name="سلات")
async def slots_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 50 or bet > 5000:
        await ctx.send("❌ الرهان: $50 - $5,000!")
        return
    if data["balance"] < bet:
        embed = emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")
        await ctx.send(embed=embed)
        return

    symbols = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🔔", "🎰"]
    weights = [25, 22, 18, 15, 8, 5, 4, 3]

    msg = await ctx.send("🎰 يدور...")
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
        title = get_funny("jackpot") if mult >= 50 else f"🎉 فزت بـ ${winnings:,}!"
        img_key = "jackpot" if mult >= 50 else "slots"
    else:
        data["balance"] -= bet
        data["total_lost"] += bet
        data["losses"] += 1
        color = C_RED
        title = "😢 حظ سيئ!"
        img_key = "slots"

    data["games_played"] += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)

    embed = emb(title, color=color, image_key=img_key)
    embed.add_field(name="🎰 النتيجة", value=f"### | {result[0]} | {result[1]} | {result[2]} |", inline=False)
    embed.add_field(name="💵 الرهان", value=f"${bet:,}", inline=True)
    embed.add_field(name="📈 المضاعف", value=f"x{mult}", inline=True)
    embed.add_field(name="💰 الأرباح", value=f"${winnings:,}", inline=True)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=False)
    if new_ach:
        embed.add_field(
            name="🏆 إنجاز جديد!",
            value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            inline=False,
        )
    await msg.edit(content=None, embed=embed)


# ───────────────────────────────────────────
# عجلة
# ───────────────────────────────────────────
@bot.command(name="عجلة")
async def wheel_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 100 or bet > 50000:
        await ctx.send("❌ الرهان: $100 - $50,000!")
        return
    if data["balance"] < bet:
        embed = emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")
        await ctx.send(embed=embed)
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
    weights = [8, 12, 15, 20, 18, 12, 8, 5, 2]

    msg = await ctx.send("🎡 تدور العجلة...")
    for _ in range(5):
        temp = random.choice(segments)
        await asyncio.sleep(0.5)
        await msg.edit(content=f"🎡 → {temp[2]} {temp[0]} ← 🎡")
    await asyncio.sleep(1)

    result = random.choices(segments, weights=weights)[0]
    label, mult, emoji, color = result
    winnings = int(bet * mult)

    if mult > 1:
        data["balance"] += winnings - bet
        data["total_earned"] += winnings - bet
        data["wins"] += 1
        text = f"🎉 ربحت **${winnings:,}**!"
    elif mult == 1:
        text = f"😊 استردت **${winnings:,}**"
        color = C_BLUE
    elif mult > 0:
        data["balance"] -= (bet - winnings)
        data["total_lost"] += (bet - winnings)
        text = f"😢 خسرت **${bet - winnings:,}**"
        color = C_ORANGE
    else:
        data["balance"] -= bet
        data["total_lost"] += bet
        data["losses"] += 1
        text = f"💀 خسرت كل شيء! **-${bet:,}**"

    data["games_played"] += 1
    data["total_gambled"] += bet
    new_ach = check_achievements(data)
    save_db(bot.db)

    embed = emb(f"🎡 عجلة الحظ — {label}", text, color, image_key="wheel")
    embed.add_field(name="💵 الرهان", value=f"${bet:,}", inline=True)
    embed.add_field(name="📈 المضاعف", value=f"x{mult}", inline=True)
    embed.add_field(name="💰 الأرباح", value=f"${winnings:,}", inline=True)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=False)
    if new_ach:
        embed.add_field(
            name="🏆 إنجاز جديد!",
            value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            inline=False,
        )
    await msg.edit(content=None, embed=embed)


# ───────────────────────────────────────────
# بلاك جاك
# ───────────────────────────────────────────
@bot.command(name="بلاكجاك")
async def blackjack_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 100 or bet > 10000:
        await ctx.send("❌ الرهان: $100 - $10,000!")
        return
    if data["balance"] < bet:
        embed = emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")
        await ctx.send(embed=embed)
        return

    suits = ["♠️", "♥️", "♦️", "♣️"]
    cards = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

    def draw():
        return (random.choice(list(cards.keys())), random.choice(suits))

    def hand_value(hand):
        val = sum(cards[c[0]] for c in hand)
        aces = sum(1 for c in hand if c[0] == "A")
        while val > 21 and aces > 0:
            val -= 10
            aces -= 1
        return val

    player = [draw(), draw()]
    dealer = [draw(), draw()]

    embed = emb("🃏 بلاك جاك", f"رهانك: **${bet:,}**", C_GREEN, image_key="blackjack")
    embed.add_field(name="يدك", value=f"{' '.join([c[0]+c[1] for c in player])} = **{hand_value(player)}**", inline=False)
    embed.add_field(name="الديلر", value=f"{dealer[0][0]}{dealer[0][1]} ❓", inline=False)

    view = discord.ui.View()
    hit_btn = discord.ui.Button(label="🃏 Hit", style=discord.ButtonStyle.primary)
    stand_btn = discord.ui.Button(label="🛑 Stand", style=discord.ButtonStyle.danger)

    async def hit_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو دورك!", ephemeral=True)
            return
        player.append(draw())
        pv = hand_value(player)
        if pv > 21:
            data["balance"] -= bet
            data["total_lost"] += bet
            data["losses"] += 1
            data["games_played"] += 1
            data["total_gambled"] += bet
            save_db(bot.db)
            e = emb(
                "💥 انفجرت!",
                f"يدك: {' '.join([c[0]+c[1] for c in player])} = **{pv}**\nخسرت **${bet:,}**",
                C_RED,
                image_key="blackjack"
            )
            e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
            await i.response.edit_message(embed=e, view=None)
        else:
            e = emb("🃏 بلاك جاك", f"رهانك: **${bet:,}**", C_GREEN, image_key="blackjack")
            e.add_field(name="يدك", value=f"{' '.join([c[0]+c[1] for c in player])} = **{pv}**", inline=False)
            e.add_field(name="الديلر", value=f"{dealer[0][0]}{dealer[0][1]} ❓", inline=False)
            await i.response.edit_message(embed=e)

    async def stand_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو دورك!", ephemeral=True)
            return
        while hand_value(dealer) < 17:
            dealer.append(draw())
        dv = hand_value(dealer)
        pv = hand_value(player)

        if dv > 21 or pv > dv:
            win = bet * 2
            data["balance"] += bet
            data["total_earned"] += bet
            data["wins"] += 1
            text = f"🎉 فزت بـ **${win:,}**!"
            color = C_GREEN
        elif pv < dv:
            data["balance"] -= bet
            data["total_lost"] += bet
            data["losses"] += 1
            text = f"😢 الديلر فاز! خسرت **${bet:,}**"
            color = C_RED
        else:
            text = f"🤝 تعادل! استردت **${bet:,}**"
            color = C_BLUE

        data["games_played"] += 1
        data["total_gambled"] += bet
        new_ach = check_achievements(data)
        save_db(bot.db)

        e = emb(f"🃏 النتيجة — {text}", "", color, image_key="blackjack")
        e.add_field(name="يدك", value=f"{' '.join([c[0]+c[1] for c in player])} = **{pv}**", inline=False)
        e.add_field(name="الديلر", value=f"{' '.join([c[0]+c[1] for c in dealer])} = **{dv}**", inline=False)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        if new_ach:
            e.add_field(
                name="🏆 إنجاز جديد!",
                value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            )
        await i.response.edit_message(embed=e, view=None)

    hit_btn.callback = hit_cb
    stand_btn.callback = stand_cb
    view.add_item(hit_btn)
    view.add_item(stand_btn)
    await ctx.send(embed=embed, view=view)

# ───────────────────────────────────────────
# تكس
# ───────────────────────────────────────────
@bot.command(name="تكس")
async def crash_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    if bet < 50 or bet > 5000:
        await ctx.send("❌ الرهان: $50 - $5,000!")
        return
    if data["balance"] < bet:
        embed = emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")
        await ctx.send(embed=embed)
        return

    multiplier = 1.0
    crash_point = random.uniform(1.1, 5.0)

    embed = emb("📈 تكس", f"رهان: **${bet:,}**\nالمضاعف: **x{multiplier:.2f}**\nاضغط **Cash Out**!", C_ORANGE, image_key="crash")
    view = discord.ui.View()
    cash_btn = discord.ui.Button(label="💰 Cash Out", style=discord.ButtonStyle.success)

    async def cash_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True)
            return
        winnings = int(bet * multiplier)
        data["balance"] += winnings - bet
        data["total_earned"] += winnings - bet
        data["wins"] += 1
        data["games_played"] += 1
        data["total_gambled"] += bet
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb(f"🎉 Cash Out! x{multiplier:.2f}", f"ربحت **${winnings:,}**", C_GREEN, image_key="crash")
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        if new_ach:
            e.add_field(
                name="🏆 إنجاز جديد!",
                value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            )
        await i.response.edit_message(embed=e, view=None)

    cash_btn.callback = cash_cb
    view.add_item(cash_btn)
    msg = await ctx.send(embed=embed, view=view)

    for _ in range(50):
        await asyncio.sleep(0.5)
        multiplier += random.uniform(0.05, 0.3)
        if multiplier >= crash_point:
            data["balance"] -= bet
            data["total_lost"] += bet
            data["losses"] += 1
            data["games_played"] += 1
            data["total_gambled"] += bet
            save_db(bot.db)
            e = emb(f"💥 انهار عند x{crash_point:.2f}!", f"خسرت **${bet:,}**", C_RED, image_key="crash")
            e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
            await msg.edit(embed=e, view=None)
            return
        embed = emb("📈 تكس", f"رهان: **${bet:,}**\nالمضاعف: **x{multiplier:.2f}**\nاضغط **Cash Out**!", C_ORANGE, image_key="crash")
        await msg.edit(embed=embed)

    winnings = int(bet * multiplier)
    data["balance"] += winnings - bet
    data["total_earned"] += winnings - bet
    data["wins"] += 1
    data["games_played"] += 1
    data["total_gambled"] += bet
    save_db(bot.db)
    e = emb(f"🎉 وصلت للحد الأقصى! x{multiplier:.2f}", f"ربحت **${winnings:,}**", C_GREEN, image_key="crash")
    e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    await msg.edit(embed=e, view=None)


# ───────────────────────────────────────────
# نهب (سرقة)
# ───────────────────────────────────────────
@bot.command(name="نهب")
async def rob_cmd(ctx, user: discord.User):
    if user.id == ctx.author.id:
        embed = emb("🤡 يا حبيبي!", get_funny("rob_self"), C_RED, image_key="rob_fail")
        await ctx.send(embed=embed)
        return

    data = get_user(bot.db, str(ctx.author.id))
    victim = get_user(bot.db, str(user.id))

    if victim["balance"] < 500:
        embed = emb("😂 فقير زيك!", get_funny("rob_poor"), C_RED, image_key="rob_fail")
        await ctx.send(embed=embed)
        return

    if data.get("protection") and datetime.fromisoformat(data["protection_expires"]) > datetime.now():
        embed = emb("🛡️ محمي!", get_funny("protection_active"), C_BLUE, image_key="protection")
        await ctx.send(embed=embed)
        return

    chance = 0.45
    if victim["balance"] > data["balance"] * 2:
        chance -= 0.15
    if data["properties"].get("cars", 0) > 0:
        chance += 0.05

    data["rob_attempts"] += 1
    if random.random() < chance:
        stolen = random.randint(int(victim["balance"] * 0.05), int(victim["balance"] * 0.25))
        victim["balance"] -= stolen
        data["balance"] += stolen
        data["total_earned"] += stolen
        data["rob_success"] += 1
        text = f"🎉 {get_funny('rob_success')}\n\nسرقت **${stolen:,}** من {user.mention}!"
        color = C_GREEN
        img_key = "rob"
    else:
        fine = random.randint(500, 2000)
        data["balance"] -= fine
        data["total_lost"] += fine
        data["rob_failed"] += 1
        text = f"{get_funny('rob_fail')}\n\n❌ تم القبض عليك! دفعت غرامة **${fine:,}**"
        color = C_RED
        img_key = "rob_fail"

    new_ach = check_achievements(data)
    save_db(bot.db)
    embed = emb("🦹 سرقة", text, color, image_key=img_key)
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    if new_ach:
        embed.add_field(
            name="🏆 إنجاز جديد!",
            value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
        )
    await ctx.send(embed=embed)


# ───────────────────────────────────────────
# حماية
# ───────────────────────────────────────────
@bot.command(name="حماية")
async def protection_cmd(ctx, hours: int = 24):
    data = get_user(bot.db, str(ctx.author.id))
    cost = hours * 500

    if data["balance"] < cost:
        embed = emb("❌ فلوسك ما تكفي!", f"تكلفة الحماية: ${cost:,}\n{get_funny('broke')}", C_RED, image_key="broke")
        await ctx.send(embed=embed)
        return

    data["balance"] -= cost
    data["protection"] = True
    data["protection_expires"] = (datetime.now() + timedelta(hours=hours)).isoformat()
    save_db(bot.db)

    embed = emb(
        "🛡️ حماية يونان فاملي!",
        f"{get_funny('protection_active')}\n\nتم تفعيل الحماية لمدة **{hours} ساعة** مقابل **${cost:,}**",
        C_BLUE,
        image_key="protection"
    )
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    embed.add_field(name="⏰ تنتهي", value=f"<t:{int((datetime.now() + timedelta(hours=hours)).timestamp())}:R>")
    await ctx.send(embed=embed)


# ───────────────────────────────────────────
# زواج
# ───────────────────────────────────────────
@bot.command(name="زواج")
async def marry_cmd(ctx, user: discord.User):
    if user.id == ctx.author.id:
        embed = emb("🪞 يا نرجسي!", get_funny("marry_self"), C_RED, image_key="marry_self")
        await ctx.send(embed=embed)
        return
    if user.bot:
        embed = emb("🤖 يا حبيبي!", get_funny("marry_bot"), C_RED, image_key="marry_bot")
        await ctx.send(embed=embed)
        return

    data = get_user(bot.db, str(ctx.author.id))
    partner = get_user(bot.db, str(user.id))

    if data["married_to"] is not None:
        embed = emb("😂 يا حبيبي!", get_funny("already_married"), C_RED, image_key="marry")
        await ctx.send(embed=embed)
        return
    if partner["married_to"] is not None:
        embed = emb("💔 للأسف!", get_funny("partner_married"), C_RED, image_key="marry")
        await ctx.send(embed=embed)
        return

    embed = emb("💍 عرض زواج يوناني!", f"{ctx.author.mention} يعرض الزواج على {user.mention}!\nالمهر: **$5,000** 💎", C_PINK, image_key="marry")
    view = discord.ui.View()
    yes_btn = discord.ui.Button(label="💍 نعم!", style=discord.ButtonStyle.success)
    no_btn = discord.ui.Button(label="❌ لا", style=discord.ButtonStyle.danger)

    async def yes_cb(i: discord.Interaction):
        if i.user.id != user.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True)
            return
        if data["balance"] < 5000:
            await i.response.send_message("❌ فلوسك ما تكفي للمهر!", ephemeral=True)
            return

        data["balance"] -= 5000
        partner["balance"] += 5000
        data["married_to"] = str(user.id)
        partner["married_to"] = str(ctx.author.id)
        data["married_since"] = datetime.now().isoformat()
        partner["married_since"] = data["married_since"]
        data["dowry"] = 5000
        partner["dowry"] = 5000
        new_ach = check_achievements(data)
        save_db(bot.db)

        e = emb("💍 زواج يوناني ناجح!", f"{ctx.author.mention} ❤️ {user.mention}\nمبروك يا عروسين! 🎉🎊", C_PINK, image_key="marry")
        if new_ach:
            e.add_field(
                name="🏆 إنجاز جديد!",
                value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
            )
        await i.response.edit_message(embed=e, view=None)

    async def no_cb(i: discord.Interaction):
        if i.user.id != user.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True)
            return
        await i.response.edit_message(
            embed=emb("💔 رفض يوناني!", f"{user.mention} رفض عرض {ctx.author.mention}!\n{get_funny('marry_self')}", C_RED, image_key="divorce"),
            view=None,
        )

    yes_btn.callba
    view.add_item(yes_btn)
    view.add_item(no_btn)
    await ctx.send(embed=embed, view=view)

# ───────────────────────────────────────────
# طلاق
# ───────────────────────────────────────────
@bot.command(name="طلاق")
async def divorce_cmd(ctx):
    data = get_user(bot.db, str(ctx.author.id))
    if data["married_to"] is None:
        embed = emb("🤣 يا حبيبي!", get_funny("not_married"), C_RED, image_key="divorce")
        await ctx.send(embed=embed)
        return

    partner_id = data["married_to"]
    partner = get_user(bot.db, partner_id)

    if data.get("last_divorce"):
        last = datetime.fromisoformat(data["last_divorce"])
        if datetime.now() - last < timedelta(hours=24):
            embed = emb("⏳ انتظر!", get_funny("divorce_cooldown"), C_RED, image_key="divorce")
            await ctx.send(embed=embed)
            return

    embed = emb("💔 طلاق يوناني", f"متأكد تبي تطلق؟\nراح تخسر نصف مهرك (${data['dowry'] // 2:,}) 💸", C_RED, image_key="divorce")
    view = discord.ui.View()
    yes_btn = discord.ui.Button(label="💔 نعم، طلق", style=discord.ButtonStyle.danger)

    async def yes_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True)
            return

        loss = data["dowry"] // 2
        data["balance"] -= loss
        partner["balance"] += loss
        data["divorce_count"] += 1
        data["last_divorce"] = datetime.now().isoformat()
        data["married_to"] = None
        partner["married_to"] = None
        data["married_since"] = None
        partner["married_since"] = None
        save_db(bot.db)

        e = emb("💔 تم الطلاق!", f"{ctx.author.mention} طلق {partner_id}\nخسر **${loss:,}** 💸", C_RED, image_key="divorce")
        await i.response.edit_message(embed=e, view=None)

    yes_btn.callback = yes_cb
    view.add_item(yes_btn)
    await ctx.send(embed=embed, view=view)


# ───────────────────────────────────────────
# ممتلكات
# ───────────────────────────────────────────
@bot.command(name="ممتلكات")
async def properties_cmd(ctx):
    data = get_user(bot.db, str(ctx.author.id))
    embed = emb("🏢 ممتلكات يونان فاملي", "استثمر وأربح دخل سلبي! 💼", C_GOLD, image_key="properties")
    for key, prop in PROPERTIES.items():
        owned = data["properties"].get(key, 0)
        embed.add_field(
            name=f"{prop['icon']} {prop['name']} (تمتلك: {owned})",
            value=f"السعر: **${prop['price']:,}**\nالدخل: **${prop['income']:,}/يوم**\n{prop['desc']}",
            inline=True,
        )

    view = discord.ui.View()
    for key, prop in PROPERTIES.items():
        btn = discord.ui.Button(
            label=f"شراء {prop['name']}",
            emoji=prop["icon"],
            style=discord.ButtonStyle.primary,
        )

        async def make_cb(k, p):
            async def cb(i: discord.Interaction):
                if i.user.id != ctx.author.id:
                    await i.response.send_message("❌ مو لك!", ephemeral=True)
                    return
                d = get_user(bot.db, str(i.user.id))
                if d["balance"] < p["price"]:
                    embed = emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")
                    await i.response.send_message(embed=embed, ephemeral=True)
                    return
                d["balance"] -= p["price"]
                d["properties"][k] = d["properties"].get(k, 0) + 1
                new_ach = check_achievements(d)
                save_db(bot.db)
                e = emb(f"✅ اشتريت {p['name']}!", f"{get_funny('buy_property')}\n\nرصيدك: ${d['balance']:,}", C_GREEN, image_key="properties")
                if new_ach:
                    e.add_field(
                        name="🏆 إنجاز جديد!",
                        value="\n".join([f"🏆 **{a['name']}** (+${a['reward']:,})" for a in new_ach]),
                    )
                await i.response.edit_message(embed=e)
            return cb

        btn.callback = make_cb(key, prop)
        view.add_item(btn)
    await ctx.send(embed=embed, view=view)


# ───────────────────────────────────────────
# تحويل
# ───────────────────────────────────────────
@bot.command(name="تحويل")
async def transfer_cmd(ctx, user: discord.User, amount: int):
    if user.id == ctx.author.id:
        embed = emb("🤣 يا حبيبي!", get_funny("transfer_self"), C_RED, image_key="transfer")
        await ctx.send(embed=embed)
        return
    if amount < 100:
        await ctx.send("❌ الحد الأدنى $100!")
        return

    data = get_user(bot.db, str(ctx.author.id))
    target = get_user(bot.db, str(user.id))

    if data["balance"] < amount:
        embed = emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")
        await ctx.send(embed=embed)
        return

    data["balance"] -= amount
    target["balance"] += amount
    data["gifts_sent"] += 1
    target["gifts_received"] += 1
    save_db(bot.db)

    embed = emb(
        "💸 تحويل يوناني ناجح!",
        f"{ctx.author.mention} → {user.mention}\nالمبلغ: **${amount:,}** 💰",
        C_GREEN,
        image_key="transfer"
    )
    embed.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    await ctx.send(embed=embed)


# ───────────────────────────────────────────
# إيداع
# ───────────────────────────────────────────
@bot.command(name="إيداع")
async def deposit_cmd(ctx, amount: int):
    data = get_user(bot.db, str(ctx.author.id))
    if amount < 100:
        await ctx.send("❌ الحد الأدنى $100!")
        return
    if data["balance"] < amount:
        embed = emb("❌ فلوسك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")
        await ctx.send(embed=embed)
        return

    data["balance"] -= amount
    data["bank"] += amount
    save_db(bot.db)

    embed = emb("🏛️ إيداع ناجح!", f"تم إيداع **${amount:,}** في البنك ✅", C_GREEN, image_key="bank")
    embed.add_field(name="🪙 اليد", value=f"${data['balance']:,}", inline=True)
    embed.add_field(name="🏛️ البنك", value=f"${data['bank']:,}", inline=True)
    await ctx.send(embed=embed)


# ───────────────────────────────────────────
# سحب
# ───────────────────────────────────────────
@bot.command(name="سحب")
async def withdraw_cmd(ctx, amount: int):
    data = get_user(bot.db, str(ctx.author.id))
    if amount < 100:
        await ctx.send("❌ الحد الأدنى $100!")
        return
    if data["bank"] < amount:
        embed = emb("❌ فلوسك في البنك ما تكفي!", get_funny("broke"), C_RED, image_key="broke")
        await ctx.send(embed=embed)
        return

    data["bank"] -= amount
    data["balance"] += amount
    save_db(bot.db)

    embed = emb("🏛️ سحب ناجح!", f"تم سحب **${amount:,}** من البنك ✅", C_GREEN, image_key="bank")
    embed.add_field(name="🪙 اليد", value=f"${data['balance']:,}", inline=True)
    embed.add_field(name="🏛️ البنك", value=f"${data['bank']:,}", inline=True)
    await ctx.send(embed=embed)


# ───────────────────────────────────────────
# مساعدة
# ───────────────────────────────────────────
@bot.command(name="مساعدة")
async def help_cmd(ctx):
    embed = emb("📖 دليل YF BANK — عائلة يونان", "أقوى بوت اقتصادي في ديسكورد! 💎", C_GOLD, image_key="help")
    cmds = [
        ("💳 -رصيد", "عرض رصيدك وممتلكاتك"),
        ("🎁 -يومي", "المكافأة اليومية"),
        ("🏆 -مطنوخين", "قائمة المطنوخين (أغنى الأعضاء)"),
        ("📊 -سوق", "سوق الموارد الحي"),
        ("🎮 -ألعاب", "قائمة الألعاب"),
        ("🎰 -سلات", "آلة الحظ"),
        ("🎡 -عجلة", "عجلة الحظ"),
        ("🃏 -بلاكجاك", "بلاك جاك 21"),
        ("📈 -تكس", "تكس — اطلع قبل الانهيار"),
        ("🦹 -نهب", "سرق مستخدم"),
        ("🛡️ -حماية", "اشتري حماية من السرقة"),
        ("💍 -زواج", "تزوج مستخدم"),
        ("💔 -طلاق", "طلق شريكك"),
        ("🏢 -ممتلكات", "اشترِ ممتلكات"),
        ("💸 -تحويل", "حول فلوس"),
        ("🏛️ -إيداع", "إيداع في البنك"),
        ("🏛️ -سحب", "سحب من البنك"),
    ]
    for name, desc in cmds:
        embed.add_field(name=name, value=desc, inline=False)
    embed.add_field(
        name="💡 نصيحة يونانية",
        value="استخدم `-يومي` كل يوم وبني سلسلة للمكافآت الإضافية! 🔥",
        inline=False,
    )
    await ctx.send(embed=embed)


# ───────────────────────────────────────────
# ابدأ / قائمة الأوامر
# ───────────────────────────────────────────
@bot.command(name="ابدأ")
async def start_cmd(ctx):
    embed = emb("🏦 YF BANK — قائمة الأوامر", "عائلة يونان ترحب بك! 👑", C_GOLD, image_key="commands")
    embed.add_field(name="🎮 الألعاب", value="سلات , عجلة , نرد , دجاجة , فواكه , قمار , بلاكجاك , تكس , حظ", inline=False)
    embed.add_field(name="💰 المال والإقتصاد", value="رصيد , يومي , إيداع , سحب , تحويل", inline=False)
    embed.add_field(name="📊 الأسواق والتداول", value="سوق , شراء , بيع , ممتلكات", inline=False)
    embed.add_field(name="👤 الحسابات", value="رصيد , مطنوخين , مستوى", inline=False)
    embed.add_field(name="🔒 الأمان", value="نهب , حماية", inline=False)
    embed.add_field(name="💍 الإجتماعية", value="زواج , طلاق", inline=False)
    embed.set_image(url=IMAGES.get("logo"))
    await ctx.send(embed=embed)


# ───────────────────────────────────────────
# مستوى
# ───────────────────────────────────────────
@bot.command(name="مستوى")
async def level_cmd(ctx, user: Optional[discord.User] = None):
    target = user or ctx.author
    data = get_user(bot.db, str(target.id))
    xp_needed = data["level"] * 1000
    xp_progress = data["xp"] % xp_needed

    embed = emb(
        f"⚡ مستوى — {target.display_name}",
        f"**{get_rank(data['level'])}** | مستوى {data['level']}",
        C_PURPLE,
        image_key="level_up"
    )
    bar = progress_bar(xp_progress, xp_needed, 20)
    embed.add_field(
        name="📊 التقدم",
        value=f"`{bar}` {xp_progress / xp_needed * 100:.1f}%\n{xp_progress:,} / {xp_needed:,} XP",
        inline=False,
    )
    embed.add_field(name="🎮 ألعاب", value=f"{data['games_played']}", inline=True)
    embed.add_field(name="🏆 فوز", value=f"{data['wins']}", inline=True)
    embed.add_field(name="💀 خسارة", value=f"{data['losses']}", inline=True)
    await ctx.send(embed=embed)

# ═══════════════════════════════════════════════════════════════════
# أحداث البوت
# ═══════════════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    print(f"YF BANK Online! {bot.user.name} ({bot.user.id})")
    print("عائلة يونان — أقوى بوت اقتصادي في ديسكورد!")
    print(f"الأوامر المتوفرة: {len(bot.commands)}")

    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="عائلة يونان | -ابدأ"
        ),
        status=discord.Status.online
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = emb(
            "❓ أمر غير معروف!",
            f"استخدم `-مساعدة` لعرض قائمة الأوامر\nأو `-ابدأ` للبدء 🎮",
            C_RED,
            image_key="help"
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = emb(
            "⚠️ ناقص معلومات!",
            f"استخدم الأمر بشكل صحيح\nاكتب `-مساعدة` للمساعدة",
            C_ORANGE,
            image_key="help"
        )
        await ctx.send(embed=embed)
    else:
        print(f"Error: {error}")


# ═══════════════════════════════════════════════════════════════════
# تشغيل البوت
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
    
