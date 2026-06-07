"""
╔══════════════════════════════════════════════════════════════════╗
║  YF BANK v2.0 - Yonan Family Discord Economy Bot                ║
║  النسخة الجديدة — أنيميشن + أزرار + كوميديا + لوحة رئيسية     ║
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

# ═══════════════════════════════════════════════════════════════════
# إعدادات أساسية
# ═══════════════════════════════════════════════════════════════════
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
if not BOT_TOKEN:
    print("❌ خطأ: ما في توكن!")
    print("📝 روح لـ Tools → Secrets في Replit")
    print("🔑 أضف: DISCORD_TOKEN = توكن_البوت")
    exit(1)

PREFIX   = "-"
DB_FILE  = "yf_bank_data.json"

C_GOLD   = 0xd4a843
C_GREEN  = 0x4ade80
C_RED    = 0xf87171
C_BLUE   = 0x60a5fa
C_PINK   = 0xff69b4
C_PURPLE = 0x9333ea
C_ORANGE = 0xf97316
C_CYAN   = 0x22d3ee
C_DARK   = 0x2b2d31

# ═══════════════════════════════════════════════════════════════════
# رسائل كوميدية
# ═══════════════════════════════════════════════════════════════════
FUNNY = {
    "broke": [
        "😂 محفظتك فاضية زي دماغك! روح اشتغل يا بطال!",
        "💀 رصيدك صفر؟ حتى الشحاذ في الشارع أغنى منك!",
        "🤣 يونان فاملي تبكي عليك! ما في فلوس يا حبيبي!",
        "😭 حتى الجثة في القبر عندها أكثر من رصيدك!",
        "🙈 محفظتك صارت تعيش في خيمة من الفقر!",
    ],
    "win": [
        "🎉 يونان فاملي فخورة فيك! ربحت يا أسد!",
        "💰 هههه الحظ حليفك اليوم! اشكر ربك!",
        "👑 مبروك يا مليونير! تذكرني لما تصير غني!",
        "🔥 يا سلام عليك! البنك بدأ يخاف منك!",
        "😎 ماشاء الله عليك! الفلوس تحبك!",
    ],
    "lose": [
        "💀 هههه راحت! يونان فاملي تقول: كان عندك فلوس!",
        "😭 خسرت؟ طبيعي أنت دايماً تخسر يا حبيبي!",
        "🤣 الفلوس ودّعتك! قالت: باي باي يا غلبان!",
        "😂 يونان فاملي تضحك عليك الحين! ولا كلمة!",
        "🙈 مسكين! روح أبكي في الحمام وارجع تحاول!",
    ],
    "jackpot": [
        "🤯 جاكبوت يونان فاملي!! صرت أغنى من المالك!",
        "💎 يا ولد! هذا مو حظ هذا سحر! مبروك!",
        "👑 الله الله! يونان فاملي تنحني لك يا ملك!",
    ],
    "rob_success": [
        "😈 يونان فاملي تقول: لص محترف! هههه!",
        "🦹 سرقتها! الضحية تبكي والبوت يضحك!",
        "🤑 مبروك! الفلوس انتقلت لصاحبها الأصلي — أنت!",
    ],
    "rob_fail": [
        "👮 الشرطة قبضت عليك يا فاشل! روح دفع الغرامة!",
        "😂 انكشفت! حتى في السرقة ما تنجح يا بطل!",
        "🚔 يونان فاملي تضحك عليك! لص فاشل من عيار أول!",
    ],
    "rob_self":   ["🤦 تسرق نفسك؟؟ يا ذكي! الفلوس في نفس المحفظة!"],
    "rob_poor":   ["😂 تسرق فقير؟ روحوا افتحوا نادي الفقراء مع بعض!"],
    "marry_bot":  ["😂 حياتك وصلت إنك تخطب بوت؟ يونان فاملي تقول: ادعوا له! 🤲😭"],
    "marry_bot_bot": ["💔 طلّقتني؟ أنا اللي كنت أحسب رصيدك وأحفظ فلوسك وأسهر عليك. وهذا جزائي؟ 😭🤖"],
    "marry_self": ["🪞 تتزوج نفسك؟ يا نرجسي! حتى نفسك ما تبيك!"],
    "already_married": ["💍 انت متزوج! يونان فاملي مو مسلسل تركي!"],
    "partner_married": ["💔 الشخص متزوج! تبي تخرب بيته؟ عيب!"],
    "not_married": ["❓ انت مو متزوج! وش بتطلق؟ الهواء؟"],
    "divorce_user": ["🤣 طلّقت؟ الحين تقدر ترجع تبكي في غرفتك بحرية! يونان فاملي تقول: كنا نراهن إنك بتطلق 🌝"],
    "marry_success": [
        "زغرودة 🎉🎊 يونان فاملي تقول: ربي يرزقكم بالذرية الصالحة ويجمعكم على خير! 🤲💍",
    ],
    "second_wife": ["👀 اووو تزوجت ثانية؟! يونان فاملي شايفاك يا شاطر! 😂 بس زوجتك الأولى بتعرف! 🌝🔥"],
    "wife_warned": ["😈 يا {wife}! زوجك تزوج ثانية وما قالك! يونان فاملي تقول: وش بتسوين فيه؟ 👀🔥"],
    "daily_streak": ["🔥 سلسلة {streak} أيام! يونان فاملي فخورة فيك يا بطل!"],
    "protection_active": ["🛡️ عندك حماية! حتى الشيطان ما يقدر يلمسك!"],
}

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
    "phones":    {"name": "هواتف",   "icon": "📱", "price": 5000,   "income": 500,   "desc": "محل إلكترونيات"},
    "stocks":    {"name": "أسهم",    "icon": "📊", "price": 10000,  "income": 1000,  "desc": "محفظة استثمارية"},
    "servers":   {"name": "سيرفرات","icon": "🖥️", "price": 20000,  "income": 2000,  "desc": "استضافة سحابية"},
    "cars":      {"name": "سيارات",  "icon": "🚗", "price": 50000,  "income": 5000,  "desc": "تأجير سيارات فاخرة"},
    "diamonds":  {"name": "ألماس",   "icon": "💎", "price": 50000,  "income": 4000,  "desc": "مناجم الألماس"},
    "lands":     {"name": "أراضي",   "icon": "🏙️", "price": 100000, "income": 8000,  "desc": "عقارات وتطوير"},
    "trains":    {"name": "قطارات",  "icon": "🚂", "price": 200000, "income": 15000, "desc": "خطوط نقل"},
    "companies": {"name": "شركات",   "icon": "💻", "price": 500000, "income": 30000, "desc": "إمبراطورية أعمال"},
}

ACHIEVEMENTS = {
    "first_win":     {"name": "أول فوز",    "desc": "اربح لعبتك الأولى",     "reward": 100,    "icon": "🏅"},
    "rich":          {"name": "غني",         "desc": "وصل لـ 100,000",        "reward": 5000,   "icon": "💰"},
    "millionaire":   {"name": "مليونير",     "desc": "وصل لـ 1,000,000",      "reward": 50000,  "icon": "💎"},
    "jackpot":       {"name": "جاكبوت",      "desc": "اربح جاكبوت السلات",    "reward": 10000,  "icon": "🎰"},
    "married":       {"name": "متزوج",       "desc": "تزوج بنجاح",            "reward": 1000,   "icon": "💍"},
    "robber":        {"name": "لص محترف",    "desc": "نجح في 10 سرقات",       "reward": 5000,   "icon": "🦹"},
    "streak_7":      {"name": "متسلسل",      "desc": "سلسلة 7 أيام",          "reward": 2000,   "icon": "🔥"},
    "streak_30":     {"name": "أسطوري",      "desc": "سلسلة 30 يوم",          "reward": 20000,  "icon": "⚡"},
    "level_10":      {"name": "نجم",         "desc": "وصل للمستوى 10",        "reward": 5000,   "icon": "⭐"},
    "level_50":      {"name": "إله",         "desc": "وصل للمستوى 50",        "reward": 100000, "icon": "👑"},
    "properties_10": {"name": "مستثمر",      "desc": "اشترِ 10 ممتلكات",      "reward": 10000,  "icon": "🏢"},
    "games_100":     {"name": "لاعب محترف",  "desc": "العب 100 لعبة",          "reward": 5000,   "icon": "🎮"},
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
            "balance": 5000, "bank": 0, "level": 1, "xp": 0, "streak": 0,
            "last_daily": None, "total_earned": 0, "total_lost": 0, "total_gambled": 0,
            "properties": {k: 0 for k in PROPERTIES},
            "inventory": {}, "married_to": None, "married_since": None, "dowry": 0,
            "divorce_count": 0, "last_divorce": None,
            "role": None, "wives": [],
            "protection": None, "protection_expires": None,
            "rob_attempts": 0, "rob_success": 0, "rob_failed": 0,
            "games_played": 0, "wins": 0, "losses": 0, "jackpots": 0,
            "achievements": [], "gifts_received": 0, "gifts_sent": 0,
            "joined": datetime.now().isoformat(), "last_active": datetime.now().isoformat(),
        }
        save_db(db)
    return db[uid]

# ═══════════════════════════════════════════════════════════════════
# إعداد البوت
# ═══════════════════════════════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class YFBank(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=intents, help_command=None)
        self.db     = load_db()
        self.market = {k: v.copy() for k, v in MARKET.items()}

    async def setup_hook(self):
        self.market_updater.start()
        self.income_collector.start()

    @tasks.loop(minutes=30)
    async def market_updater(self):
        for item in self.market.values():
            change = random.uniform(-0.15, 0.15)
            item["buy"]  = max(50,  int(item["buy"]  * (1 + change)))
            item["sell"] = max(25,  int(item["sell"] * (1 + change)))
            if item["sell"] >= item["buy"]:
                item["sell"] = int(item["buy"] * 0.88)

    @tasks.loop(hours=24)
    async def income_collector(self):
        for uid, data in self.db.items():
            income = sum(data["properties"].get(k, 0) * p["income"] for k, p in PROPERTIES.items())
            if income > 0:
                data["balance"]      += income
                data["total_earned"] += income
        save_db(self.db)

    @market_updater.before_loop
    @income_collector.before_loop
    async def before_loops(self):
        await self.wait_until_ready()

bot = YFBank()

# ═══════════════════════════════════════════════════════════════════
# دوال مساعدة
# ═══════════════════════════════════════════════════════════════════
def emb(title, desc="", color=C_GOLD):
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now())
    e.set_footer(text="🏦 YF BANK 2026 | عائلة يونان 👑")
    return e

def funny(key, **kw):
    msgs = FUNNY.get(key, ["🤔"])
    return random.choice(msgs).format(**kw)

def fmt(n):
    if n >= 1_000_000_000: return f"{n/1_000_000_000:.1f}B"
    if n >= 1_000_000:     return f"{n/1_000_000:.1f}M"
    if n >= 1_000:         return f"{n/1_000:.1f}K"
    return str(n)

def get_rank(lvl):
    ranks = [
        (0,  "🪨 مبتدئ"),   (10, "🥉 تاجر"),
        (20, "🥈 مستثمر"),  (30, "🥇 مليونير"),
        (50, "💎 أسطورة"),  (100,"👑 إله يوناني"),
    ]
    r = ranks[0][1]
    for threshold, name in ranks:
        if lvl >= threshold: r = name
    return r

def progress_bar(cur, total, length=15):
    if total == 0: return "░" * length
    filled = int(length * cur / total)
    return "█" * filled + "░" * (length - filled)

def check_achievements(data):
    new, done = [], set(data.get("achievements", []))
    checks = [
        ("first_win",     data["wins"] >= 1),
        ("rich",          data["balance"] + data["bank"] >= 100_000),
        ("millionaire",   data["balance"] + data["bank"] >= 1_000_000),
        ("married",       data["married_to"] is not None),
        ("robber",        data.get("rob_success", 0) >= 10),
        ("streak_7",      data["streak"] >= 7),
        ("streak_30",     data["streak"] >= 30),
        ("level_10",      data["level"] >= 10),
        ("level_50",      data["level"] >= 50),
        ("properties_10", sum(data["properties"].values()) >= 10),
        ("games_100",     data["games_played"] >= 100),
    ]
    for key, cond in checks:
        if cond and key not in done:
            ach = ACHIEVEMENTS[key]
            new.append(ach)
            data["achievements"].append(key)
            data["balance"] += ach["reward"]
    return new

def add_ach(embed, new_ach):
    if new_ach:
        lines = "\n".join(f"{a['icon']} **{a['name']}** — +${a['reward']:,}" for a in new_ach)
        embed.add_field(name="🏆 إنجازات جديدة!", value=lines, inline=False)

def add_xp(data, amount=50):
    data["xp"] += amount
    leveled = False
    while data["xp"] >= data["level"] * 1000:
        data["xp"]    -= data["level"] * 1000
        data["level"] += 1
        leveled = True
    return leveled

# ═══════════════════════════════════════════════════════════════════
# الأحداث
# ═══════════════════════════════════════════════════════════════════
@bot.event
async def on_ready():
    print(f"✅ YF BANK v2.0 شغّال! {bot.user.name}")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="عائلة يونان | -ابدأ"),
        status=discord.Status.online
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return  # تجاهل كلياً لو القناة غلط
    if isinstance(error, commands.CommandNotFound):
        if ctx.channel.id != BANK_CHANNEL_ID:
            return  # تجاهل في القنوات الثانية
        await ctx.send(embed=emb("❓ أمر غير موجود!", "اكتب **-ابدأ** أو **-مساعدة** 📖", C_RED))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=emb("⚠️ ناقص معلومات!", "تأكد من كتابة الأمر صح.", C_ORANGE))
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=emb("⚠️ خطأ في المدخلات!", "أدخل أرقام صحيحة.", C_ORANGE))
    else:
        print(f"Error: {error}")

# ═══════════════════════════════════════════════════════════════════
# لوحة رئيسية
# ═══════════════════════════════════════════════════════════════════
class MainMenuView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx

    async def interaction_check(self, i):
        if i.user.id != self.ctx.author.id:
            await i.response.send_message("❌ هذي مش لوحتك!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="💰 رصيدي", style=discord.ButtonStyle.success, row=0)
    async def balance_btn(self, i, _):
        await i.response.defer()
        await balance_cmd(self.ctx)

    @discord.ui.button(label="🎁 يومي", style=discord.ButtonStyle.primary, row=0)
    async def daily_btn(self, i, _):
        await i.response.defer()
        await daily_cmd(self.ctx)

    @discord.ui.button(label="🏆 مطنوخين", style=discord.ButtonStyle.secondary, row=0)
    async def top_btn(self, i, _):
        await i.response.defer()
        await top_cmd(self.ctx)

    @discord.ui.button(label="🎮 ألعاب", style=discord.ButtonStyle.danger, row=1)
    async def games_btn(self, i, _):
        await i.response.edit_message(embed=build_games_embed(), view=GamesMenuView(self.ctx))

    @discord.ui.button(label="📊 سوق", style=discord.ButtonStyle.secondary, row=1)
    async def market_btn(self, i, _):
        await i.response.edit_message(embed=build_market_embed(bot), view=MarketMenuView(self.ctx))

    @discord.ui.button(label="🏢 ممتلكات", style=discord.ButtonStyle.secondary, row=1)
    async def props_btn(self, i, _):
        await i.response.edit_message(embed=build_props_embed(), view=PropertiesView(self.ctx))

    @discord.ui.button(label="🛡️ حماية", style=discord.ButtonStyle.secondary, row=2)
    async def prot_btn(self, i, _):
        await i.response.edit_message(embed=build_protection_embed(), view=ProtectionView(self.ctx))

    @discord.ui.button(label="💍 زواج / طلاق", style=discord.ButtonStyle.secondary, row=2)
    async def marry_btn(self, i, _):
        await i.response.send_message("💍 استخدم: `-زواج @شخص` أو `-طلاق`", ephemeral=True)

    @discord.ui.button(label="📖 مساعدة", style=discord.ButtonStyle.secondary, row=2)
    async def help_btn(self, i, _):
        await i.response.edit_message(embed=build_help_embed(), view=HelpView(self.ctx))

def build_main_embed(ctx):
    data  = get_user(bot.db, str(ctx.author.id))
    total = data["balance"] + data["bank"]
    e = emb(
        f"🏦 YF BANK — مرحباً {ctx.author.display_name}!",
        f"## 💰 ${fmt(total)}\n{get_rank(data['level'])} | مستوى {data['level']} | 🔥 {data['streak']} يوم",
        C_GOLD
    )
    e.add_field(name="🪙 اليد",    value=f"${fmt(data['balance'])}", inline=True)
    e.add_field(name="🏛️ البنك",  value=f"${fmt(data['bank'])}",    inline=True)
    e.add_field(name="🎮 ألعاب",  value=f"{data['games_played']}", inline=True)
    e.add_field(name="🏆 فوز",    value=f"{data['wins']}",          inline=True)
    e.add_field(name="💀 خسارة",  value=f"{data['losses']}",        inline=True)
    e.add_field(name="🏢 ممتلكات",value=f"{sum(data['properties'].values())}", inline=True)
    bar = progress_bar(data["xp"] % (data["level"]*1000), data["level"]*1000, 20)
    e.add_field(name="⚡ XP", value=f"`{bar}`", inline=False)
    return e

@bot.command(name="ابدأ")
async def start_cmd(ctx):
    await ctx.send(embed=build_main_embed(ctx), view=MainMenuView(ctx))

# ═══════════════════════════════════════════════════════════════════
# قائمة الألعاب
# ═══════════════════════════════════════════════════════════════════
def build_games_embed():
    e = emb("🎮 ألعاب يونان فاملي", "اختر لعبتك وادخل رهانك! 🔥", C_PURPLE)
    games_info = [
        ("🎰 سلات",     "-سلات [رهان]",     "$50 - $5,000"),
        ("🎡 عجلة",     "-عجلة [رهان]",     "$100 - $50,000"),
        ("🎲 نرد",      "-نرد [رهان]",      "$100 - $10,000"),
        ("🐔 دجاجة",    "-دجاجة [رهان]",    "$50 - $2,000"),
        ("🎨 ألوان",    "-ألوان [رهان]",    "$50 - $5,000"),
        ("🍎 فواكه",    "-فواكه [رهان]",    "$50 - $3,000"),
        ("📦 صناديق",   "-صناديق [رهان]",   "$100 - $10,000"),
        ("🃏 قمار",     "-قمار [رهان]",     "$100 - $50,000"),
        ("🃏 بلاكجاك",  "-بلاكجاك [رهان]", "$100 - $10,000"),
        ("📈 تكس",      "-تكس [رهان]",      "$50 - $5,000"),
        ("🍀 حظ",       "-حظ [رهان]",       "$10 - $1,000"),
        ("🐉 تنين",     "-تنين [رهان]",     "$100 - $20,000"),
    ]
    for name, cmd, limit in games_info:
        e.add_field(name=name, value=f"`{cmd}`\n{limit}", inline=True)
    return e

class GamesMenuView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx

    async def interaction_check(self, i):
        if i.user.id != self.ctx.author.id:
            await i.response.send_message("❌ مش لوحتك!", ephemeral=True); return False
        return True

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, i, _):
        await i.response.edit_message(embed=build_main_embed(self.ctx), view=MainMenuView(self.ctx))

# ═══════════════════════════════════════════════════════════════════
# السوق
# ═══════════════════════════════════════════════════════════════════
def build_market_embed(bot_instance):
    e = emb("📊 سوق YF — الأسعار الحية", "تتغير كل 30 دقيقة 💹", C_CYAN)
    for key, item in bot_instance.market.items():
        orig   = MARKET[key]["buy"]
        change = ((item["buy"] - orig) / orig) * 100
        arrow  = "🟢📈" if change >= 0 else "🔴📉"
        e.add_field(
            name=f"{item['icon']} {item['name']}",
            value=f"{arrow}\nشراء: `${fmt(item['buy'])}`\nبيع: `${fmt(item['sell'])}`\nتغير: `{change:+.1f}%`",
            inline=True,
        )
    return e

class MarketMenuView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.selected_item = None

        self.select = discord.ui.Select(
            placeholder="🛒 اختر سلعة...",
            options=[
                discord.SelectOption(label=v["name"], value=k)
                for k, v in MARKET.items()
            ]
        )
        self.select.callback = self.select_cb
        self.add_item(self.select)

    async def interaction_check(self, i):
        if i.user.id != self.ctx.author.id:
            await i.response.send_message("❌ مش لوحتك!", ephemeral=True); return False
        return True

    async def select_cb(self, i: discord.Interaction):
        self.selected_item = i.data["values"][0]
        item = bot.market[self.selected_item]
        e = emb(
            f"{item['icon']} {item['name']}",
            f"شراء: **${item['buy']:,}**\nبيع: **${item['sell']:,}**\n\nكم وحدة تبي؟",
            C_CYAN
        )
        await i.response.edit_message(embed=e, view=MarketQuantityView(self.ctx, self.selected_item))

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary, row=1)
    async def back(self, i, _):
        await i.response.edit_message(embed=build_main_embed(self.ctx), view=MainMenuView(self.ctx))

class MarketQuantityView(discord.ui.View):
    def __init__(self, ctx, item_key):
        super().__init__(timeout=60)
        self.ctx      = ctx
        self.item_key = item_key

    async def interaction_check(self, i):
        if i.user.id != self.ctx.author.id:
            await i.response.send_message("❌ مش لوحتك!", ephemeral=True); return False
        return True

    async def do_buy(self, i, amount):
        data = get_user(bot.db, str(self.ctx.author.id))
        item = bot.market[self.item_key]
        cost = item["buy"] * amount
        if data["balance"] < cost:
            await i.response.send_message(f"❌ {funny('broke')}\nتحتاج: ${cost:,}", ephemeral=True); return
        data["balance"] -= cost
        data["inventory"][self.item_key] = data["inventory"].get(self.item_key, 0) + amount
        save_db(bot.db)
        e = emb("✅ تم الشراء!", f"اشتريت **{amount}x {item['name']}** بـ **${cost:,}**\n🪙 رصيدك: ${data['balance']:,}", C_GREEN)
        await i.response.edit_message(embed=e, view=MarketBackView(self.ctx))

    @discord.ui.button(label="x1", style=discord.ButtonStyle.primary, row=0)
    async def buy1(self, i, _): await self.do_buy(i, 1)

    @discord.ui.button(label="x5", style=discord.ButtonStyle.primary, row=0)
    async def buy5(self, i, _): await self.do_buy(i, 5)

    @discord.ui.button(label="x10", style=discord.ButtonStyle.primary, row=0)
    async def buy10(self, i, _): await self.do_buy(i, 10)

    @discord.ui.button(label="x50", style=discord.ButtonStyle.success, row=0)
    async def buy50(self, i, _): await self.do_buy(i, 50)

    async def do_sell(self, i, amount):
        data  = get_user(bot.db, str(self.ctx.author.id))
        item  = bot.market[self.item_key]
        owned = data["inventory"].get(self.item_key, 0)
        sell_amt = min(amount, owned)
        if sell_amt == 0:
            await i.response.send_message("❌ ما عندك شيء تبيعه!", ephemeral=True); return
        earn = item["sell"] * sell_amt
        data["inventory"][self.item_key] -= sell_amt
        data["balance"]      += earn
        data["total_earned"] += earn
        save_db(bot.db)
        e = emb("✅ تم البيع!", f"بعت **{sell_amt}x {item['name']}** بـ **${earn:,}**\n🪙 رصيدك: ${data['balance']:,}", C_GREEN)
        await i.response.edit_message(embed=e, view=MarketBackView(self.ctx))

    @discord.ui.button(label="بيع x1", style=discord.ButtonStyle.danger, row=1)
    async def sell1(self, i, _): await self.do_sell(i, 1)

    @discord.ui.button(label="بيع x5", style=discord.ButtonStyle.danger, row=1)
    async def sell5(self, i, _): await self.do_sell(i, 5)

    @discord.ui.button(label="بيع الكل", style=discord.ButtonStyle.danger, row=1)
    async def sell_all(self, i, _):
        data = get_user(bot.db, str(self.ctx.author.id))
        await self.do_sell(i, data["inventory"].get(self.item_key, 0))

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary, row=2)
    async def back(self, i, _):
        await i.response.edit_message(embed=build_market_embed(bot), view=MarketMenuView(self.ctx))

class MarketBackView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    @discord.ui.button(label="📊 السوق", style=discord.ButtonStyle.secondary)
    async def to_market(self, i, _):
        await i.response.edit_message(embed=build_market_embed(bot), view=MarketMenuView(self.ctx))

    @discord.ui.button(label="🏠 الرئيسية", style=discord.ButtonStyle.primary)
    async def to_main(self, i, _):
        await i.response.edit_message(embed=build_main_embed(self.ctx), view=MainMenuView(self.ctx))

# ═══════════════════════════════════════════════════════════════════
# الممتلكات
# ═══════════════════════════════════════════════════════════════════
def build_props_embed():
    e = emb("🏢 سوق الممتلكات", "استثمر وجمع دخل يومي تلقائي! 💼", C_BLUE)
    for key, p in PROPERTIES.items():
        e.add_field(
            name=f"{p['icon']} {p['name']}",
            value=f"سعر: `${fmt(p['price'])}`\nدخل: `${fmt(p['income'])}/يوم`\n{p['desc']}",
            inline=True
        )
    return e

class PropertiesView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx

        self.select = discord.ui.Select(
            placeholder="🏢 اختر ممتلك...",
            options=[
                discord.SelectOption(label=v["name"], value=k, description=f"${fmt(v['price'])} | دخل ${fmt(v['income'])}/يوم")
                for k, v in PROPERTIES.items()
            ]
        )
        self.select.callback = self.select_cb
        self.add_item(self.select)

    async def interaction_check(self, i):
        if i.user.id != self.ctx.author.id:
            await i.response.send_message("❌ مش لوحتك!", ephemeral=True); return False
        return True

    async def select_cb(self, i: discord.Interaction):
        key  = i.data["values"][0]
        prop = PROPERTIES[key]
        data = get_user(bot.db, str(self.ctx.author.id))
        owned = data["properties"].get(key, 0)
        e = emb(
            f"{prop['icon']} {prop['name']}",
            f"السعر: **${prop['price']:,}**\nالدخل اليومي: **${prop['income']:,}**\n{prop['desc']}\n\nعندك: **{owned}**",
            C_BLUE
        )
        await i.response.edit_message(embed=e, view=BuyPropertyView(self.ctx, key))

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary, row=1)
    async def back(self, i, _):
        await i.response.edit_message(embed=build_main_embed(self.ctx), view=MainMenuView(self.ctx))

class BuyPropertyView(discord.ui.View):
    def __init__(self, ctx, key):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.key = key

    async def interaction_check(self, i):
        if i.user.id != self.ctx.author.id:
            await i.response.send_message("❌ مش لوحتك!", ephemeral=True); return False
        return True

    async def do_buy(self, i, amount):
        data = get_user(bot.db, str(self.ctx.author.id))
        prop = PROPERTIES[self.key]
        cost = prop["price"] * amount
        if data["balance"] < cost:
            await i.response.send_message(f"❌ {funny('broke')}\nتحتاج: ${cost:,}", ephemeral=True); return
        data["balance"] -= cost
        data["properties"][self.key] = data["properties"].get(self.key, 0) + amount
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb("✅ تم الشراء!", f"{funny('protection_active')}\nاشتريت **{amount}x {prop['name']}** بـ **${cost:,}**\n🪙 رصيدك: ${data['balance']:,}", C_GREEN)
        add_ach(e, new_ach)
        await i.response.edit_message(embed=e, view=PropertiesView(self.ctx))

    @discord.ui.button(label="شراء x1", style=discord.ButtonStyle.success, row=0)
    async def buy1(self, i, _): await self.do_buy(i, 1)

    @discord.ui.button(label="شراء x3", style=discord.ButtonStyle.success, row=0)
    async def buy3(self, i, _): await self.do_buy(i, 3)

    @discord.ui.button(label="شراء x5", style=discord.ButtonStyle.success, row=0)
    async def buy5(self, i, _): await self.do_buy(i, 5)

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary, row=1)
    async def back(self, i, _):
        await i.response.edit_message(embed=build_props_embed(), view=PropertiesView(self.ctx))

# ═══════════════════════════════════════════════════════════════════
# الحماية
# ═══════════════════════════════════════════════════════════════════
def build_protection_embed():
    e = emb("🛡️ حماية يونان فاملي", "احمي نفسك من السرقة! 🔒", C_BLUE)
    options = [(6, 3000), (12, 5500), (24, 10000), (48, 18000), (72, 25000), (168, 50000)]
    for h, cost in options:
        e.add_field(name=f"⏰ {h} ساعة", value=f"${cost:,}", inline=True)
    return e

class ProtectionView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    async def interaction_check(self, i):
        if i.user.id != self.ctx.author.id:
            await i.response.send_message("❌ مش لوحتك!", ephemeral=True); return False
        return True

    async def buy_protection(self, i, hours, cost):
        data = get_user(bot.db, str(self.ctx.author.id))
        if data["balance"] < cost:
            await i.response.send_message(f"❌ {funny('broke')}\nتحتاج: ${cost:,}", ephemeral=True); return
        data["balance"]           -= cost
        data["protection"]         = True
        data["protection_expires"] = (datetime.now() + timedelta(hours=hours)).isoformat()
        save_db(bot.db)
        e = emb("🛡️ تم تفعيل الحماية!", f"{funny('protection_active')}\n\nمحمي لمدة **{hours} ساعة**\nالتكلفة: **${cost:,}**\n🪙 رصيدك: ${data['balance']:,}", C_BLUE)
        await i.response.edit_message(embed=e, view=BackToMainView(self.ctx))

    @discord.ui.button(label="6 ساعات — $3,000", style=discord.ButtonStyle.primary, row=0)
    async def p6(self, i, _): await self.buy_protection(i, 6, 3000)

    @discord.ui.button(label="12 ساعة — $5,500", style=discord.ButtonStyle.primary, row=0)
    async def p12(self, i, _): await self.buy_protection(i, 12, 5500)

    @discord.ui.button(label="24 ساعة — $10,000", style=discord.ButtonStyle.success, row=1)
    async def p24(self, i, _): await self.buy_protection(i, 24, 10000)

    @discord.ui.button(label="48 ساعة — $18,000", style=discord.ButtonStyle.success, row=1)
    async def p48(self, i, _): await self.buy_protection(i, 48, 18000)

    @discord.ui.button(label="أسبوع — $50,000", style=discord.ButtonStyle.danger, row=2)
    async def p168(self, i, _): await self.buy_protection(i, 168, 50000)

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary, row=2)
    async def back(self, i, _):
        await i.response.edit_message(embed=build_main_embed(self.ctx), view=MainMenuView(self.ctx))

@bot.command(name="حماية")
async def protection_cmd(ctx, hours: int = 0):
    if hours < 1 or hours > 1000:
        await ctx.send(embed=emb("🛡️ الحماية", "اكتب: `-حماية [عدد الساعات]`\nمثال: `-حماية 24`\n\n💰 السعر: **$300 لكل ساعة**", C_BLUE)); return

    data = get_user(bot.db, str(ctx.author.id))
    cost = hours * 300

    # تحقق لو عنده حماية شغالة
    if data.get("protection_expires"):
        expires = datetime.fromisoformat(data["protection_expires"])
        if expires > datetime.now():
            remaining = expires - datetime.now()
            hrs_left = int(remaining.total_seconds() // 3600)
            await ctx.send(embed=emb("🛡️ عندك حماية!", f"الحماية شغالة لمدة **{hrs_left} ساعة** باقية!\nما تحتاج تجدد الحين.", C_BLUE)); return

    e = emb(
        "🛡️ تأكيد الحماية",
        f"⏰ **{hours} ساعة**\n💰 **السعر: ${cost:,}**\n🪙 رصيدك: ${data['balance']:,}",
        C_BLUE
    )
    view = discord.ui.View(timeout=30)
    yes = discord.ui.Button(label=f"✅ اشتري ${cost:,}", style=discord.ButtonStyle.success)
    no  = discord.ui.Button(label="❌ إلغاء", style=discord.ButtonStyle.danger)

    async def yes_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        if data["balance"] < cost:
            await i.response.send_message(f"❌ {funny('broke')}\nتحتاج: ${cost:,}", ephemeral=True); return
        data["balance"]           -= cost
        data["protection"]         = True
        data["protection_expires"] = (datetime.now() + timedelta(hours=hours)).isoformat()
        save_db(bot.db)
        e2 = emb("🛡️ تم تفعيل الحماية!", f"{funny('protection_active')}\n\n⏰ محمي لمدة **{hours} ساعة**\n💰 دفعت: **${cost:,}**\n🪙 رصيدك: ${data['balance']:,}", C_BLUE)
        await i.response.edit_message(embed=e2, view=None)

    async def no_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        await i.response.edit_message(embed=emb("❌ إلغاء", "تم الإلغاء!", C_RED), view=None)

    yes.callback = yes_cb
    no.callback  = no_cb
    view.add_item(yes)
    view.add_item(no)
    await ctx.send(embed=e, view=view)
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    @discord.ui.button(label="🏠 الرئيسية", style=discord.ButtonStyle.primary)
    async def to_main(self, i, _):
        await i.response.edit_message(embed=build_main_embed(self.ctx), view=MainMenuView(self.ctx))

# ═══════════════════════════════════════════════════════════════════
# المساعدة
# ═══════════════════════════════════════════════════════════════════
def build_help_embed():
    e = emb("📖 دليل YF BANK v2.0", "اختر قسم للتفاصيل 👇", C_GOLD)
    e.add_field(name="🎮 الألعاب",    value="سلات، عجلة، نرد، دجاجة، ألوان، فواكه، صناديق، قمار، بلاكجاك، تكس، حظ، تنين", inline=False)
    e.add_field(name="👁️ العين",      value="-عين @شخص — تصيبه العين وتتحول بعد 10 ثواني!", inline=False)
    e.add_field(name="💰 المال",      value="رصيد، يومي، إيداع، سحب، تحويل", inline=False)
    e.add_field(name="📊 التداول",    value="سوق، شراء، بيع", inline=False)
    e.add_field(name="🏢 الاستثمار", value="ممتلكات — دخل يومي تلقائي", inline=False)
    e.add_field(name="🔒 الأمان",     value="نهب، حماية", inline=False)
    e.add_field(name="💍 الاجتماعية", value="زواج، طلاق", inline=False)
    e.add_field(name="💡 نصيحة",     value="استخدم `-ابدأ` للوحة الرئيسية بالأزرار!", inline=False)
    return e

class HelpView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=60)
        self.ctx = ctx

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, i, _):
        await i.response.edit_message(embed=build_main_embed(self.ctx), view=MainMenuView(self.ctx))

@bot.command(name="مساعدة")
async def help_cmd(ctx):
    await ctx.send(embed=build_help_embed())

# ═══════════════════════════════════════════════════════════════════
# رصيد
# ═══════════════════════════════════════════════════════════════════
@bot.command(name="رصيد")
async def balance_cmd(ctx, user: Optional[discord.User] = None):
    target = user or ctx.author
    data   = get_user(bot.db, str(target.id))
    total  = data["balance"] + data["bank"]
    xp_needed  = data["level"] * 1000
    xp_progress = data["xp"] % xp_needed if xp_needed else 0
    data["last_active"] = datetime.now().isoformat()
    save_db(bot.db)

    note = f"\n\n{funny('broke')}" if total < 1000 else ""
    e = emb(
        f"💳 محفظة {target.display_name} {'👑' if data['level'] >= 30 else ''}",
        f"## 💰 ${fmt(total)}{note}",
        C_GOLD
    )
    bar = progress_bar(xp_progress, xp_needed, 20)
    pct = f"{xp_progress/xp_needed*100:.1f}%" if xp_needed else "0%"
    e.add_field(name=f"⚡ {get_rank(data['level'])} | Lv{data['level']}", value=f"`{bar}` {pct}", inline=False)
    e.add_field(name="🪙 اليد",    value=f"${fmt(data['balance'])}",               inline=True)
    e.add_field(name="🏛️ البنك",  value=f"${fmt(data['bank'])}",                  inline=True)
    e.add_field(name="📉 خسارة",   value=f"${fmt(data.get('total_lost', 0))}",      inline=True)
    e.add_field(name="🎮 ألعاب",   value=f"{data['games_played']}",                 inline=True)
    e.add_field(name="🏆 فوز",    value=f"{data['wins']}",                          inline=True)
    e.add_field(name="🔥 سلسلة",  value=f"{data['streak']} يوم",                    inline=True)
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════════════
# يومي
# ═══════════════════════════════════════════════════════════════════
@bot.command(name="يومي")
async def daily_cmd(ctx):
    data = get_user(bot.db, str(ctx.author.id))
    now  = datetime.now()
    if data["last_daily"]:
        diff = now - datetime.fromisoformat(data["last_daily"])
        if diff < timedelta(hours=24):
            rem = timedelta(hours=24) - diff
            h   = int(rem.total_seconds() // 3600)
            m   = int((rem.total_seconds() % 3600) // 60)
            await ctx.send(embed=emb("⏳ بكره!", f"ارجع بعد **{h}س {m}د** ⏰\n{funny('broke')}", C_RED))
            return
        data["streak"] = 1 if diff > timedelta(hours=48) else data["streak"] + 1
    else:
        data["streak"] = 1

    base   = 1000
    streak = min(data["streak"] * 100, 5000)
    level  = data["level"] * 50
    total  = base + streak + level
    data["balance"]      += total
    data["last_daily"]    = now.isoformat()
    data["total_earned"] += total
    leveled = add_xp(data, 100)
    new_ach = check_achievements(data)
    save_db(bot.db)

    e = emb("🎁 مكافأة اليوم!", f"✅ استلمت فلوسك يا غالي!", C_GREEN)
    e.add_field(name="💰 أساسية",  value=f"${base:,}",                         inline=True)
    e.add_field(name="🔥 سلسلة",   value=f"+${streak:,} (x{data['streak']})",  inline=True)
    e.add_field(name="⚡ مستوى",   value=f"+${level:,}",                        inline=True)
    e.add_field(name="💎 الإجمالي",value=f"**${total:,}**",                     inline=False)
    e.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}",               inline=True)
    e.add_field(name="🔥 سلسلة",   value=f"**{data['streak']} أيام**",          inline=True)
    if data["streak"] > 1:
        e.add_field(name="🎯 يونان فاملي تقول:", value=funny("daily_streak", streak=data["streak"]), inline=False)
    if leveled:
        e.add_field(name="⚡ مستوى جديد!", value=f"وصلت للمستوى **{data['level']}**! {funny('win')}", inline=False)
    add_ach(e, new_ach)
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════════════
# مطنوخين
# ═══════════════════════════════════════════════════════════════════
@bot.command(name="مطنوخين")
async def top_cmd(ctx):
    users_data = [
        (m, d["balance"] + d["bank"], d["level"])
        for uid, d in bot.db.items()
        if (m := ctx.guild.get_member(int(uid)))
    ]
    users_data.sort(key=lambda x: x[1], reverse=True)

    e = emb("🏆 قائمة المطنوخين — عائلة يونان", "أغنى وأقوى أعضاء العائلة! 💎", C_GOLD)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    crowns = ["👑","💎","🥉","🌟","⭐","✨","🔥","💫","🎯","🎪"]
    for i, (member, total, lvl) in enumerate(users_data[:10]):
        e.add_field(
            name=f"{medals[i]} {crowns[i]} {member.display_name}",
            value=f"💰 ${fmt(total)} | ⚡ Lv{lvl} | {get_rank(lvl)}",
            inline=False
        )

    view = discord.ui.View()
    btn = discord.ui.Button(label="🏠 الرئيسية", style=discord.ButtonStyle.primary)
    async def go_main(i):
        if i.user.id != ctx.author.id: await i.response.send_message("❌", ephemeral=True); return
        await i.response.edit_message(embed=build_main_embed(ctx), view=MainMenuView(ctx))
    btn.callback = go_main
    view.add_item(btn)
    await ctx.send(embed=e, view=view)

# ═══════════════════════════════════════════════════════════════════
# إيداع / سحب / تحويل
# ═══════════════════════════════════════════════════════════════════
@bot.command(name="إيداع")
async def deposit_cmd(ctx, amount: int):
    data = get_user(bot.db, str(ctx.author.id))
    if amount < 100:
        await ctx.send("❌ الحد الأدنى $100!"); return
    if data["balance"] < amount:
        await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
    data["balance"] -= amount
    data["bank"]    += amount
    save_db(bot.db)
    e = emb("🏛️ إيداع ناجح!", f"أودعت **${amount:,}** في البنك ✅", C_GREEN)
    e.add_field(name="🪙 اليد",   value=f"${data['balance']:,}", inline=True)
    e.add_field(name="🏛️ البنك", value=f"${data['bank']:,}",    inline=True)
    await ctx.send(embed=e)

@bot.command(name="سحب")
async def withdraw_cmd(ctx, amount: int):
    data = get_user(bot.db, str(ctx.author.id))
    if amount < 100:
        await ctx.send("❌ الحد الأدنى $100!"); return
    if data["bank"] < amount:
        await ctx.send(embed=emb("❌ البنك ما يكفي!", funny("broke"), C_RED)); return
    data["bank"]    -= amount
    data["balance"] += amount
    save_db(bot.db)
    e = emb("🏛️ سحب ناجح!", f"سحبت **${amount:,}** من البنك ✅", C_GREEN)
    e.add_field(name="🪙 اليد",   value=f"${data['balance']:,}", inline=True)
    e.add_field(name="🏛️ البنك", value=f"${data['bank']:,}",    inline=True)
    await ctx.send(embed=e)

@bot.command(name="تحويل")
async def transfer_cmd(ctx, user: discord.User, amount: int):
    if user.id == ctx.author.id:
        await ctx.send(embed=emb("🤡 يا ذكي!", "تحول لنفسك؟ الفلوس في نفس المحفظة!", C_RED)); return
    if amount < 1:
        await ctx.send("❌ الحد الأدنى $1!"); return
    data   = get_user(bot.db, str(ctx.author.id))
    target = get_user(bot.db, str(user.id))
    if data["balance"] < amount:
        await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
    data["balance"]       -= amount
    target["balance"]     += amount
    data["gifts_sent"]    += 1
    target["gifts_received"] += 1
    save_db(bot.db)
    e = emb("💸 تحويل ناجح!", f"{ctx.author.mention} ➡️ {user.mention}\n**${amount:,}** 💰", C_GREEN)
    e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════════════
# مستوى
# ═══════════════════════════════════════════════════════════════════
@bot.command(name="مستوى")
async def level_cmd(ctx, user: Optional[discord.User] = None):
    target = user or ctx.author
    data   = get_user(bot.db, str(target.id))
    xp_needed  = data["level"] * 1000
    xp_progress = data["xp"] % xp_needed if xp_needed else 0
    bar = progress_bar(xp_progress, xp_needed, 20)
    pct = f"{xp_progress/xp_needed*100:.1f}%" if xp_needed else "0%"
    e = emb(f"⚡ مستوى — {target.display_name}", f"**{get_rank(data['level'])}** | مستوى {data['level']}", C_PURPLE)
    e.add_field(name="📊 التقدم", value=f"`{bar}` {pct}\n{xp_progress:,} / {xp_needed:,} XP", inline=False)
    e.add_field(name="🎮 ألعاب",  value=f"{data['games_played']}", inline=True)
    e.add_field(name="🏆 فوز",   value=f"{data['wins']}",          inline=True)
    e.add_field(name="💀 خسارة", value=f"{data['losses']}",        inline=True)
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════════════
# نهب
# ═══════════════════════════════════════════════════════════════════
@bot.command(name="نهب")
async def rob_cmd(ctx, user: discord.User):
    if user.id == ctx.author.id:
        await ctx.send(embed=emb("🤦 يا ذكي!", funny("rob_self"), C_RED)); return
    data   = get_user(bot.db, str(ctx.author.id))
    victim = get_user(bot.db, str(user.id))
    if victim["balance"] < 500:
        await ctx.send(embed=emb("😂 فقير!", funny("rob_poor"), C_RED)); return
    if victim.get("protection_expires"):
        if datetime.fromisoformat(victim["protection_expires"]) > datetime.now():
            await ctx.send(embed=emb("🛡️ محمي!", "الضحية عندها حماية يونان فاملي!", C_BLUE)); return
    chance = 0.45
    if victim["balance"] > data["balance"] * 2: chance -= 0.15
    if data["properties"].get("cars", 0) > 0:   chance += 0.05
    data["rob_attempts"] += 1

    msg = await ctx.send("🦹 يحاول يسرق...")
    await asyncio.sleep(0.5)
    for anim in ["🦹 يتسلل...", "🏃 يركض نحو الضحية...", "👜 يخطف المحفظة..."]:
        await asyncio.sleep(0.6)
        await msg.edit(content=anim)
    await asyncio.sleep(0.8)

    if random.random() < chance:
        stolen = random.randint(int(victim["balance"] * 0.05), int(victim["balance"] * 0.25))
        victim["balance"]    -= stolen
        data["balance"]      += stolen
        data["total_earned"] += stolen
        data["rob_success"]  += 1
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb("🦹 سرقة ناجحة!", f"{funny('rob_success')}\n\nسرقت **${stolen:,}** من {user.mention}! 😈", C_GREEN)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        add_ach(e, new_ach)
        await msg.edit(content=None, embed=e)
    else:
        fine = random.randint(500, 2000)
        data["balance"]    -= max(0, min(fine, data["balance"]))
        data["total_lost"] += fine
        data["rob_failed"] += 1
        save_db(bot.db)
        e = emb("👮 انقبضت!", f"{funny('rob_fail')}\n\nغرامة: **${fine:,}**", C_RED)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        await msg.edit(content=None, embed=e)

# ═══════════════════════════════════════════════════════════════════
# زواج / طلاق
# ═══════════════════════════════════════════════════════════════════
@bot.command(name="زواج")
async def marry_cmd(ctx, user: discord.User, dowry: int = 0):
    if user.id == ctx.author.id:
        await ctx.send(embed=emb("🪞 يا نرجسي!", funny("marry_self"), C_RED)); return
    if user.bot:
        await ctx.send(embed=emb("🤖 يا حبيبي!", funny("marry_bot"), C_RED)); return

    data    = get_user(bot.db, str(ctx.author.id))
    partner = get_user(bot.db, str(user.id))

    # الزوجة ما تقدر تتزوج ثاني
    if data.get("role") == "wife":
        await ctx.send(embed=emb("🚫 ما تقدرين!", "أنتِ زوجة! الزوجة ما تتزوج ثاني 👀", C_RED)); return

    # الشريك إذا كان متزوج
    if partner["married_to"]:
        await ctx.send(embed=emb("💔 للأسف!", funny("partner_married"), C_RED)); return

    # تحقق من المهر
    if dowry < 200:
        await ctx.send(embed=emb("❌ المهر قليل!", f"الحد الأدنى للمهر **$200**!\nاكتب: `-زواج @شخص [المهر]`\nمثال: `-زواج @شخص 1000`", C_RED)); return

    DOWRY = dowry
    is_second = data["married_to"] is not None

    # رد البوت حسب المهر
    if DOWRY < 1000:
        dowry_comment = "😂 المهر كذا؟! اهرب يا عروس اهرب! هذا ما يكفي حتى لعشاء واحد! 💀🤲"
        dowry_color   = C_RED
    elif DOWRY < 3000:
        dowry_comment = "🌝 لا فقير لا غني.. زي الطقس في أبريل! مو حار مو بارد! 😐"
        dowry_color   = C_ORANGE
    else:
        dowry_comment = "👑 اقبلي يا عروس قبل ما يصحى من نومه ويغير رأيه! 🎊💎😂"
        dowry_color   = C_GREEN

    # ── المرحلة الأولى: عرض المهر ──
    e_dowry = emb(
        "💰 المهر أولاً!",
        f"{ctx.author.mention} تبي تتزوج {user.mention}\n\n"
        f"💍 **المهر:** ${DOWRY:,}\n"
        f"🪙 **رصيدك الحالي:** ${data['balance']:,}\n\n"
        f"{dowry_comment}\n\n"
        f"{'⚠️ زواج ثاني! زوجتك الأولى بتعرف! 🌝' if is_second else ''}",
        dowry_color
    )
    view_dowry = discord.ui.View(timeout=60)
    pay_btn    = discord.ui.Button(label=f"💰 ادفع المهر ${DOWRY:,}", style=discord.ButtonStyle.success)
    cancel_btn = discord.ui.Button(label="❌ إلغاء", style=discord.ButtonStyle.danger)

    async def pay_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        if data["balance"] < DOWRY:
            await i.response.send_message(
                embed=emb("❌ ما في فلوس!", f"تحتاج **${DOWRY:,}** للمهر!\nرصيدك: ${data['balance']:,} 😂", C_RED),
                ephemeral=True
            ); return

        # خصم المهر مؤقتاً وانتظار القبول
        data["balance"] -= DOWRY
        save_db(bot.db)

        # ── المرحلة الثانية: عرض الزواج للشريك ──
        if is_second:
            e2 = emb("💍 عرض زواج ثاني!", f"👀 {ctx.author.mention} يعرض الزواج على {user.mention}!\nدفع المهر: **${DOWRY:,}** ✅\n\n⚠️ زوجتك الأولى بتعرف! 🌝", C_PINK)
        else:
            e2 = emb("💍 عرض زواج!", f"{ctx.author.mention} يعرض الزواج على {user.mention}!\nدفع المهر: **${DOWRY:,}** ✅ 💎", C_PINK)

        view2   = discord.ui.View(timeout=60)
        yes_btn = discord.ui.Button(label="💍 نعم قبلت!", style=discord.ButtonStyle.success)
        no_btn  = discord.ui.Button(label="❌ رفضت",      style=discord.ButtonStyle.danger)

        async def yes_cb(i2: discord.Interaction):
            if i2.user.id != user.id:
                await i2.response.send_message("❌ مو لك!", ephemeral=True); return

            partner["balance"] += DOWRY
            first_wife_id = data["married_to"]
            data["role"]    = "husband"
            partner["role"] = "wife"

            if is_second:
                if "wives" not in data: data["wives"] = []
                data["wives"].append(str(user.id))
                partner["married_to"] = str(ctx.author.id)
            else:
                data["married_to"]    = str(user.id)
                partner["married_to"] = str(ctx.author.id)
                data["married_since"] = partner["married_since"] = datetime.now().isoformat()
                data["dowry"]         = partner["dowry"] = DOWRY

            new_ach = check_achievements(data)
            save_db(bot.db)

            e3 = emb("💍 زواج ناجح! 🎊", f"{ctx.author.mention} ❤️ {user.mention}\n\n{funny('marry_success')}", C_PINK)
            e3.set_image(url="https://cdn.discordapp.com/attachments/1498329259507319015/1513242467825352926/Screenshot_------_com.anthropic.claude-edit.jpg?ex=6a27045f&is=6a25b2df&hm=8966c4d1f3c51102deb130d5f201e319e847203e6666fcabd2659e2d00dfbe16&")
            add_ach(e3, new_ach)
            await i2.response.edit_message(embed=e3, view=None)

            # أبلّغ الزوجة الأولى لو زواج ثاني
            if is_second and first_wife_id:
                try:
                    first_wife = await bot.fetch_user(int(first_wife_id))
                    warn_e = emb("🔥 يونان فاملي تقول!", funny("wife_warned").replace("{wife}", first_wife.mention), C_RED)
                    await ctx.send(content=first_wife.mention, embed=warn_e)
                except: pass
            if is_second:
                await ctx.send(embed=emb("👀 بوت يقول!", funny("second_wife"), C_ORANGE))

        async def no_cb(i2: discord.Interaction):
            if i2.user.id != user.id:
                await i2.response.send_message("❌ مو لك!", ephemeral=True); return
            # رجّع المهر
            data["balance"] += DOWRY
            save_db(bot.db)
            e3 = emb("💔 رُفض!", f"{user.mention} رفض/ت {ctx.author.mention}! 😂\n💰 رجع لك المهر **${DOWRY:,}**", C_RED)
            await i2.response.edit_message(embed=e3, view=None)

        yes_btn.callback = yes_cb
        no_btn.callback  = no_cb
        view2.add_item(yes_btn)
        view2.add_item(no_btn)
        await i.response.edit_message(embed=e2, view=view2)

    async def cancel_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لك!", ephemeral=True); return
        await i.response.edit_message(embed=emb("❌ إلغاء", "تم الإلغاء!", C_RED), view=None)

    pay_btn.callback    = pay_cb
    cancel_btn.callback = cancel_cb
    view_dowry.add_item(pay_btn)
    view_dowry.add_item(cancel_btn)
    await ctx.send(embed=e_dowry, view=view_dowry)

@bot.command(name="طلاق")
async def divorce_cmd(ctx, user: discord.User = None):
    # لازم يمنشن
    if user is None:
        await ctx.send(embed=emb("❓ منشن زوجك!", "اكتب: `-طلاق @شخص`", C_RED)); return

    # طلاق البوت — مباشرة بدون تحقق
    if user.bot:
        await ctx.send(embed=emb("💔 طلّقت البوت؟!", funny("marry_bot_bot"), C_RED)); return

    data = get_user(bot.db, str(ctx.author.id))

    # الزوجة ما تطلق
    if data.get("role") == "wife":
        await ctx.send(embed=emb("🚫 ما تقدرين!", "الزوجة ما تطلّق! قولي لزوجك يطلقك 😂", C_RED)); return

    # تحقق إنه فعلاً متزوج
    if not data["married_to"] and not data.get("wives"):
        await ctx.send(embed=emb("❓ انت مو متزوج!", funny("not_married"), C_RED)); return

    # تحقق إن المنشن هو زوجه فعلاً
    wives_list = data.get("wives", [])
    is_main_wife   = data["married_to"] == str(user.id)
    is_second_wife = str(user.id) in wives_list

    if not is_main_wife and not is_second_wife:
        await ctx.send(embed=emb("😂 هذا مو زوجك!", f"{user.mention} مو متزوج منك! شايف غلط؟ 👀", C_RED)); return

    # تنفيذ الطلاق
    partner = get_user(bot.db, str(user.id))
    partner["married_to"] = None
    partner["role"]       = None

    if is_second_wife:
        data["wives"].remove(str(user.id))
    else:
        data["married_to"] = None
        data["role"]       = None

    data["divorce_count"] = data.get("divorce_count", 0) + 1
    save_db(bot.db)

    e = emb("💔 طلاق!", funny("divorce_user"), C_RED)
    e.add_field(name="💔 المطلّق/ة", value=user.mention)
    e.set_image(url="https://cdn.discordapp.com/attachments/1498329259507319015/1513242245619388506/Screenshot_------_com.anthropic.claude-edit.jpg?ex=6a27042a&is=6a25b2aa&hm=be7f8441670a0cd67f99a43739a05eda628e9ac08c63440a7febc0f8ea4e80b3&")
    await ctx.send(embed=e)

# ═══════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════
# الألعاب
# ═══════════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════

def game_check(data, bet, min_bet, max_bet):
    """Returns error string or None"""
    if bet < min_bet or bet > max_bet:
        return f"❌ الرهان: ${min_bet:,} - ${max_bet:,}!"
    if data["balance"] < bet:
        return f"❌ {funny('broke')}"
    return None

def apply_win(data, bet, mult):
    win = int(bet * mult) - bet
    data["balance"]      += win
    data["total_earned"] += win
    data["wins"]         += 1

def apply_loss(data, bet):
    data["balance"]    -= bet
    data["total_lost"] += bet
    data["losses"]     += 1

def finish_game(data, bet):
    data["games_played"]  += 1
    data["total_gambled"] += bet

# ───────────────────────────────────────────────────────────────────
# سلات
# ───────────────────────────────────────────────────────────────────
@bot.command(name="سلات")
async def slots_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 50, 5000)
    if err: await ctx.send(err); return

    symbols = ["🍒","🍋","🍊","🍇","💎","7️⃣","🔔","🎰"]
    weights  = [25, 22, 18, 15,  8,   5,   4,   3]

    msg = await ctx.send("🎰 ┃ ❓ ┃ ❓ ┃ ❓ ┃")
    for step in range(1, 4):
        await asyncio.sleep(0.5)
        t = random.choices(symbols, weights=weights, k=3)
        shown = " ┃ ".join(t[:step] + ["❓"] * (3 - step))
        await msg.edit(content=f"🎰 ┃ {shown} ┃")
    await asyncio.sleep(0.5)

    result = random.choices(symbols, weights=weights, k=3)
    mult   = 0
    if result[0] == result[1] == result[2]:
        mult = {"💎": 100, "7️⃣": 50, "🔔": 25, "🎰": 20}.get(result[0], 10)
    elif len(set(result)) < 3:
        mult = 2

    data["balance"] -= bet
    if mult > 0:
        apply_win(data, bet, mult)
        if mult >= 50: data["jackpots"] += 1
        color   = C_GOLD if mult >= 50 else C_GREEN
        title   = funny("jackpot") if mult >= 50 else funny("win")
        img_key = "jackpot"
    else:
        apply_loss(data, bet)
        color, title = C_RED, funny("lose")

    finish_game(data, bet)
    new_ach = check_achievements(data)
    save_db(bot.db)

    winnings = int(bet * mult)
    e = emb(title, color=color)
    e.add_field(name="🎰 النتيجة", value=f"┃ {result[0]} ┃ {result[1]} ┃ {result[2]} ┃", inline=False)
    e.add_field(name="💵 الرهان",  value=f"${bet:,}",       inline=True)
    e.add_field(name="📈 مضاعف",   value=f"x{mult}",         inline=True)
    e.add_field(name="💰 الأرباح", value=f"${winnings:,}",  inline=True)
    e.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}", inline=False)
    add_ach(e, new_ach)
    await msg.edit(content=None, embed=e)

# ───────────────────────────────────────────────────────────────────
# عجلة
# ───────────────────────────────────────────────────────────────────
@bot.command(name="عجلة")
async def wheel_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 100, 50000)
    if err: await ctx.send(err); return

    segments = [
        ("0x 💀",   0.0,  C_RED),
        ("0.5x 🔴", 0.5,  C_RED),
        ("0.8x ⚫", 0.8,  C_ORANGE),
        ("1x 🔵",   1.0,  C_BLUE),
        ("1.5x 🟢", 1.5,  C_GREEN),
        ("2x 💚",   2.0,  C_GREEN),
        ("3x 🌟",   3.0,  C_GOLD),
        ("5x ✨",   5.0,  C_GOLD),
        ("10x 💎",  10.0, C_PURPLE),
    ]
    weights = [8, 12, 15, 20, 18, 12, 8, 5, 2]

    wheel_frames = ["🎡 ━ ❓ ━ ❓ ━ ❓ ━ 🎡",
                    "🎡 ━ 2x ━ 0x ━ 5x ━ 🎡",
                    "🎡 ━ 0x ━ 3x ━ 1x ━ 🎡",
                    "🎡 ━ 5x ━ 1x ━ 0x ━ 🎡",
                    "🎡 ━ 1x ━ 2x ━ 3x ━ 🎡"]
    msg = await ctx.send(wheel_frames[0])
    for f in wheel_frames[1:]:
        await asyncio.sleep(0.45)
        await msg.edit(content=f)
    await asyncio.sleep(0.7)

    label, mult, color = random.choices(segments, weights=weights)[0]
    winnings = int(bet * mult)
    data["balance"] -= bet

    if mult > 1:
        apply_win(data, bet, mult)
        text = f"{funny('win')}\n🎉 ربحت **${winnings:,}**!"
    elif mult == 1:
        data["balance"] += bet
        text  = f"😊 استردت **${winnings:,}**"
        color = C_BLUE
    elif mult > 0:
        loss = bet - winnings
        data["balance"]    += winnings
        data["total_lost"] += loss
        text  = f"😢 خسرت **${loss:,}**"
        color = C_ORANGE
    else:
        apply_loss(data, bet)
        data["balance"] += bet
        data["balance"] -= bet
        text = f"{funny('lose')}\n💀 خسرت كل شيء! **-${bet:,}**"

    finish_game(data, bet)
    new_ach = check_achievements(data)
    save_db(bot.db)

    e = emb(f"🎡 {label}", text, color)
    e.add_field(name="💵 الرهان",  value=f"${bet:,}",      inline=True)
    e.add_field(name="📈 مضاعف",   value=f"x{mult}",        inline=True)
    e.add_field(name="💰 الأرباح", value=f"${winnings:,}", inline=True)
    e.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}", inline=False)
    add_ach(e, new_ach)
    await msg.edit(content=None, embed=e)

# ───────────────────────────────────────────────────────────────────
# نرد
# ───────────────────────────────────────────────────────────────────
@bot.command(name="نرد")
async def dice_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 100, 10000)
    if err: await ctx.send(err); return

    dice_faces = ["⚀","⚁","⚂","⚃","⚄","⚅"]
    msg = await ctx.send("🎲 يرمي النرد...")
    for _ in range(3):
        await asyncio.sleep(0.5)
        pr = random.choice(dice_faces)
        br = random.choice(dice_faces)
        await msg.edit(content=f"🎲 أنت: {pr} | البوت: {br}")
    await asyncio.sleep(0.6)

    player_roll = random.randint(1, 6)
    bot_roll    = random.randint(1, 6)
    pr_face = dice_faces[player_roll - 1]
    br_face = dice_faces[bot_roll - 1]

    if player_roll > bot_roll:
        data["balance"]      += bet
        data["total_earned"] += bet
        data["wins"]         += 1
        color, text, winnings = C_GREEN, f"{funny('win')}\n🎉 {player_roll} > {bot_roll}", bet * 2
    elif player_roll < bot_roll:
        data["balance"]    -= bet
        data["total_lost"] += bet
        data["losses"]     += 1
        color, text, winnings = C_RED, f"{funny('lose')}\n😢 {player_roll} < {bot_roll}", 0
    else:
        color, text, winnings = C_BLUE, f"🤝 تعادل! {player_roll} = {bot_roll}", bet

    finish_game(data, bet)
    new_ach = check_achievements(data)
    save_db(bot.db)

    e = emb("🎲 نتيجة النرد", text, color)
    e.add_field(name="🎲 أنت",    value=f"{pr_face} ({player_roll})", inline=True)
    e.add_field(name="🤖 البوت",  value=f"{br_face} ({bot_roll})",    inline=True)
    e.add_field(name="💵 الرهان", value=f"${bet:,}",                  inline=True)
    e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}",      inline=False)
    add_ach(e, new_ach)
    await msg.edit(content=None, embed=e)

# ───────────────────────────────────────────────────────────────────
# قمار
# ───────────────────────────────────────────────────────────────────
@bot.command(name="قمار")
async def gamble_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 100, 50000)
    if err: await ctx.send(err); return

    msg = await ctx.send("🃏 يقلّب الورقة...")
    for face in ["🂠", "🂡", "🂢", "🂣"]:
        await asyncio.sleep(0.4)
        await msg.edit(content=f"🃏 {face}")
    await asyncio.sleep(0.5)

    win = random.random() < 0.5
    if win:
        data["balance"]      += bet
        data["total_earned"] += bet
        data["wins"]         += 1
        e = emb("🃏 فزت!", f"{funny('win')}\n🎉 ربحت **${bet*2:,}**!", C_GREEN)
    else:
        data["balance"]    -= bet
        data["total_lost"] += bet
        data["losses"]     += 1
        e = emb("🃏 خسرت!", f"{funny('lose')}\n😢 خسرت **${bet:,}**!", C_RED)

    finish_game(data, bet)
    new_ach = check_achievements(data)
    save_db(bot.db)
    e.add_field(name="💵 الرهان", value=f"${bet:,}",            inline=True)
    e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=True)
    add_ach(e, new_ach)
    await msg.edit(content=None, embed=e)

# ───────────────────────────────────────────────────────────────────
# حظ
# ───────────────────────────────────────────────────────────────────
@bot.command(name="حظ")
async def luck_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 10, 1000)
    if err: await ctx.send(err); return

    msg = await ctx.send("🍀 تفحص حظك...")
    for anim in ["🍀 🌟 🍀", "🌟 🍀 🌟", "🍀 ⭐ 🍀"]:
        await asyncio.sleep(0.4)
        await msg.edit(content=anim)
    await asyncio.sleep(0.5)

    outcomes = [(0, 30), (0.5, 25), (1, 20), (2, 12), (3, 7), (5, 4), (10, 2)]
    mult     = random.choices([o[0] for o in outcomes], weights=[o[1] for o in outcomes])[0]
    winnings = int(bet * mult)

    if mult > 1:
        apply_win(data, bet, mult)
        color, title, text = C_GREEN, f"🍀 حظ x{mult}!", f"{funny('win')}\n🎉 ربحت **${winnings:,}**!"
    elif mult == 1:
        color, title, text = C_BLUE, "🍀 حظ عادي!", f"😊 استردت **${bet:,}**"
    else:
        apply_loss(data, bet)
        color, title, text = C_RED, "🍀 حظ سيئ!", f"{funny('lose')}\n😢 خسرت **${bet - winnings:,}**"

    finish_game(data, bet)
    new_ach = check_achievements(data)
    save_db(bot.db)
    e = emb(title, text, color)
    e.add_field(name="💵 الرهان",  value=f"${bet:,}",         inline=True)
    e.add_field(name="📈 مضاعف",   value=f"x{mult}",           inline=True)
    e.add_field(name="🪙 رصيدك",  value=f"${data['balance']:,}", inline=True)
    add_ach(e, new_ach)
    await msg.edit(content=None, embed=e)

# ───────────────────────────────────────────────────────────────────
# دجاجة
# ───────────────────────────────────────────────────────────────────
@bot.command(name="دجاجة")
async def chicken_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 50, 2000)
    if err: await ctx.send(err); return

    multiplier = [1.0]
    data["balance"] -= bet
    stopped = [False]

    def make_embed():
        return emb(
            "🐔 لعبة الدجاجة",
            f"رهانك: **${bet:,}**\nالمضاعف: **x{multiplier[0]:.2f}**\nالأرباح المحتملة: **${int(bet*multiplier[0]):,}**\n\n⚠️ إذا ماتت الدجاجة تخسر كل شيء!",
            C_ORANGE
        )

    view = discord.ui.View(timeout=60)
    cont = discord.ui.Button(label="🐔 استمر", style=discord.ButtonStyle.primary)
    cash = discord.ui.Button(label="💰 اطلع!", style=discord.ButtonStyle.success)

    async def cont_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
        if stopped[0]: return

        if random.random() < 0.30:
            stopped[0] = True
            data["total_lost"]  += bet
            data["losses"]      += 1
            finish_game(data, bet)
            save_db(bot.db)
            e = emb("🐔 الدجاجة ماتت! 💀", f"{funny('lose')}\n💀 خسرت **${bet:,}**!\nكان المضاعف x{multiplier[0]:.2f}", C_RED)
            e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
            await i.response.edit_message(embed=e, view=None)
        else:
            multiplier[0] = round(multiplier[0] + random.uniform(0.2, 0.5), 2)
            await i.response.edit_message(embed=make_embed())

    async def cash_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
        if stopped[0]: return
        stopped[0] = True
        winnings = int(bet * multiplier[0])
        data["balance"]      += winnings
        data["total_earned"] += winnings - bet
        data["wins"]         += 1
        finish_game(data, bet)
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb(f"🐔 اطلعت! x{multiplier[0]:.2f}", f"{funny('win')}\n🎉 ربحت **${winnings:,}**!", C_GREEN)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        add_ach(e, new_ach)
        await i.response.edit_message(embed=e, view=None)

    cont.callback = cont_cb
    cash.callback = cash_cb
    view.add_item(cont)
    view.add_item(cash)
    await ctx.send(embed=make_embed(), view=view)

# ───────────────────────────────────────────────────────────────────
# ألوان
# ───────────────────────────────────────────────────────────────────
@bot.command(name="ألوان")
async def colors_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 50, 5000)
    if err: await ctx.send(err); return

    colors_list = [("🔴 أحمر", "red"), ("🔵 أزرق", "blue"), ("🟢 أخضر", "green"), ("🟡 أصفر", "yellow")]
    e = emb("🎨 لعبة الألوان", f"رهانك: **${bet:,}**\nخمّن اللون الصحيح واربح x2! 🎯", C_PURPLE)
    view = discord.ui.View()
    chosen = [False]

    for label, value in colors_list:
        btn = discord.ui.Button(label=label, style=discord.ButtonStyle.secondary)
        async def make_cb(v, lbl):
            async def cb(i: discord.Interaction):
                if i.user.id != ctx.author.id:
                    await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
                if chosen[0]: return
                chosen[0] = True
                winning = random.choice([c[1] for c in colors_list])
                win_lbl = next(l for l, val in colors_list if val == winning)
                if v == winning:
                    data["balance"]      += bet
                    data["total_earned"] += bet
                    data["wins"]         += 1
                    color = C_GREEN
                    text  = f"{funny('win')}\n🎉 ربحت **${bet*2:,}**!"
                    title = f"🎨 صح! {lbl}"
                else:
                    data["balance"]    -= bet
                    data["total_lost"] += bet
                    data["losses"]     += 1
                    color = C_RED
                    text  = f"{funny('lose')}\n😢 خسرت **${bet:,}**\nكان: {win_lbl}"
                    title = f"🎨 غلط! {win_lbl}"
                finish_game(data, bet)
                new_ach = check_achievements(data)
                save_db(bot.db)
                e2 = emb(title, text, color)
                e2.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
                add_ach(e2, new_ach)
                await i.response.edit_message(embed=e2, view=None)
            return cb
        btn.callback = await make_cb(value, label)
        view.add_item(btn)

    await ctx.send(embed=e, view=view)

# ───────────────────────────────────────────────────────────────────
# فواكه
# ───────────────────────────────────────────────────────────────────
@bot.command(name="فواكه")
async def fruits_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 50, 3000)
    if err: await ctx.send(err); return

    fruits = ["🍎","🍊","🍋","🍇","🍓","🍑","🥝","🍒"]

    msg = await ctx.send("🍎 يخلط الفواكه...")
    for _ in range(3):
        await asyncio.sleep(0.5)
        t = [random.choice(fruits) for _ in range(9)]
        await msg.edit(content=f"┃ {t[0]} ┃ {t[1]} ┃ {t[2]} ┃\n┃ {t[3]} ┃ {t[4]} ┃ {t[5]} ┃\n┃ {t[6]} ┃ {t[7]} ┃ {t[8]} ┃")
    await asyncio.sleep(0.5)

    row1 = random.choices(fruits, k=3)
    row2 = random.choices(fruits, k=3)
    row3 = random.choices(fruits, k=3)

    matches = sum(1 for r in [row1, row2, row3] if r[0]==r[1]==r[2])
    if matches == 3:    mult, title = 10, "🍎 ثلاثي مثالي!"
    elif matches == 2:  mult, title = 5,  "🍎 مزدوج ممتاز!"
    elif matches == 1:  mult, title = 2,  "🍎 مطابقة واحدة!"
    else:               mult, title = 0,  "🍎 ما في مطابقة!"

    winnings = bet * mult
    if mult > 0:
        apply_win(data, bet, mult)
        color = C_GREEN
        text  = f"{funny('win')}\n🎉 ربحت **${winnings:,}**!"
    else:
        apply_loss(data, bet)
        color = C_RED
        text  = f"{funny('lose')}\n😢 خسرت **${bet:,}**"

    finish_game(data, bet)
    new_ach = check_achievements(data)
    save_db(bot.db)

    e = emb(title, text, color)
    e.add_field(name="صف 1", value=" ┃ ".join(row1), inline=False)
    e.add_field(name="صف 2", value=" ┃ ".join(row2), inline=False)
    e.add_field(name="صف 3", value=" ┃ ".join(row3), inline=False)
    e.add_field(name="📈 مضاعف",  value=f"x{mult}",         inline=True)
    e.add_field(name="💰 أرباح",  value=f"${winnings:,}",  inline=True)
    e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}", inline=True)
    add_ach(e, new_ach)
    await msg.edit(content=None, embed=e)

# ───────────────────────────────────────────────────────────────────
# صناديق
# ───────────────────────────────────────────────────────────────────
@bot.command(name="صناديق")
async def boxes_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 100, 10000)
    if err: await ctx.send(err); return

    prizes = [
        ("💀 فارغ!",   0,   35),
        ("😐 صغير",   0.5,  25),
        ("😊 عادي",   1.5,  20),
        ("🎉 جيد",    2,    12),
        ("💎 ممتاز",  5,     6),
        ("👑 جاكبوت", 10,    2),
    ]
    e = emb("📦 اختر صندوق!", f"رهانك: **${bet:,}**\n4 صناديق — واحد فيه الجائزة! 🎁", C_BLUE)
    view = discord.ui.View()
    opened = [False]

    for idx in range(4):
        btn = discord.ui.Button(label=f"📦 {idx+1}", style=discord.ButtonStyle.primary)
        async def make_cb():
            async def cb(i: discord.Interaction):
                if i.user.id != ctx.author.id:
                    await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
                if opened[0]: return
                opened[0] = True
                prize_label, mult, _ = random.choices(prizes, weights=[p[2] for p in prizes])[0]
                winnings = int(bet * mult)
                if mult > 1:
                    apply_win(data, bet, mult)
                    color = C_GREEN
                    text  = f"{funny('win')}\n🎉 {prize_label} — ربحت **${winnings:,}**!"
                elif mult > 0:
                    data["balance"]    += winnings - bet
                    data["total_lost"] += bet - winnings
                    color = C_ORANGE
                    text  = f"{prize_label} استردت **${winnings:,}**"
                else:
                    apply_loss(data, bet)
                    color = C_RED
                    text  = f"{funny('lose')}\n{prize_label} خسرت **${bet:,}**"
                finish_game(data, bet)
                new_ach = check_achievements(data)
                save_db(bot.db)
                e2 = emb("📦 فتحت الصندوق!", text, color)
                e2.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
                add_ach(e2, new_ach)
                await i.response.edit_message(embed=e2, view=None)
            return cb
        btn.callback = await make_cb()
        view.add_item(btn)

    await ctx.send(embed=e, view=view)

# ───────────────────────────────────────────────────────────────────
# بلاكجاك
# ───────────────────────────────────────────────────────────────────
@bot.command(name="بلاكجاك")
async def blackjack_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 100, 10000)
    if err: await ctx.send(err); return

    suits = ["♠️","♥️","♦️","♣️"]
    vals  = {"A":11,"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10}

    def draw():   return (random.choice(list(vals.keys())), random.choice(suits))
    def hval(hand):
        v, aces = sum(vals[c[0]] for c in hand), sum(1 for c in hand if c[0]=="A")
        while v > 21 and aces: v -= 10; aces -= 1
        return v

    player = [draw(), draw()]
    dealer = [draw(), draw()]

    def render():
        e = emb("🃏 بلاك جاك", f"رهانك: **${bet:,}**\nالفوز = 21 أو أكثر من الديلر!", C_GREEN)
        e.add_field(name="🃏 يدك",   value=f"{'  '.join(c[0]+c[1] for c in player)} = **{hval(player)}**", inline=False)
        e.add_field(name="🤖 الديلر",value=f"{dealer[0][0]}{dealer[0][1]} ❓", inline=False)
        return e

    done = [False]
    view = discord.ui.View()
    hit  = discord.ui.Button(label="🃏 Hit",   style=discord.ButtonStyle.primary)
    stand= discord.ui.Button(label="🛑 Stand", style=discord.ButtonStyle.danger)

    async def hit_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو دورك!", ephemeral=True); return
        if done[0]: return
        player.append(draw())
        pv = hval(player)
        if pv > 21:
            done[0] = True
            data["balance"]    -= bet
            data["total_lost"] += bet
            data["losses"]     += 1
            finish_game(data, bet)
            save_db(bot.db)
            e = emb("💥 انفجرت!", f"{funny('lose')}\n😢 يدك = {pv} — خسرت **${bet:,}**", C_RED)
            e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
            await i.response.edit_message(embed=e, view=None)
        else:
            await i.response.edit_message(embed=render())

    async def stand_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو دورك!", ephemeral=True); return
        if done[0]: return
        done[0] = True
        while hval(dealer) < 17: dealer.append(draw())
        dv, pv = hval(dealer), hval(player)
        if dv > 21 or pv > dv:
            data["balance"]      += bet
            data["total_earned"] += bet
            data["wins"]         += 1
            text, color = f"{funny('win')}\n🎉 فزت بـ **${bet*2:,}**!", C_GREEN
        elif pv < dv:
            data["balance"]    -= bet
            data["total_lost"] += bet
            data["losses"]     += 1
            text, color = f"{funny('lose')}\n😢 الديلر فاز! خسرت **${bet:,}**", C_RED
        else:
            text, color = f"🤝 تعادل! استردت **${bet:,}**", C_BLUE
        finish_game(data, bet)
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb("🃏 النتيجة", text, color)
        e.add_field(name="🃏 يدك",    value=f"{'  '.join(c[0]+c[1] for c in player)} = **{pv}**", inline=False)
        e.add_field(name="🤖 الديلر", value=f"{'  '.join(c[0]+c[1] for c in dealer)} = **{dv}**", inline=False)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        add_ach(e, new_ach)
        await i.response.edit_message(embed=e, view=None)

    hit.callback   = hit_cb
    stand.callback = stand_cb
    view.add_item(hit)
    view.add_item(stand)
    await ctx.send(embed=render(), view=view)

# ───────────────────────────────────────────────────────────────────
# تكس (Crash)
# ───────────────────────────────────────────────────────────────────
@bot.command(name="تكس")
async def crash_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 50, 5000)
    if err: await ctx.send(err); return

    multiplier  = [1.0]
    crash_point = round(random.uniform(1.05, 10.0), 2)
    cashed_out  = [False]

    def make_embed():
        bar_len = min(int(multiplier[0] * 3), 20)
        bar = "🟩" * bar_len + "⬛" * (20 - bar_len)
        return emb(
            f"📈 تكس — x{multiplier[0]:.2f}",
            f"رهان: **${bet:,}**\n`{bar}`\n\n⚠️ اضغط **Cash Out** قبل الانهيار!",
            C_ORANGE
        )

    view    = discord.ui.View()
    cash_btn= discord.ui.Button(label="💰 Cash Out!", style=discord.ButtonStyle.success)

    async def cash_cb(i: discord.Interaction):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
        if cashed_out[0]: return
        cashed_out[0] = True
        winnings = int(bet * multiplier[0])
        data["balance"]      += winnings - bet
        data["total_earned"] += winnings - bet
        data["wins"]         += 1
        finish_game(data, bet)
        new_ach = check_achievements(data)
        save_db(bot.db)
        e = emb(f"💰 Cash Out! x{multiplier[0]:.2f}", f"{funny('win')}\n🎉 ربحت **${winnings:,}**", C_GREEN)
        e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
        add_ach(e, new_ach)
        await i.response.edit_message(embed=e, view=None)

    cash_btn.callback = cash_cb
    view.add_item(cash_btn)
    msg = await ctx.send(embed=make_embed(), view=view)

    for _ in range(80):
        await asyncio.sleep(0.4)
        if cashed_out[0]: return
        multiplier[0] = round(multiplier[0] + random.uniform(0.04, 0.25), 2)
        if multiplier[0] >= crash_point:
            if not cashed_out[0]:
                cashed_out[0] = True
                data["balance"]    -= bet
                data["total_lost"] += bet
                data["losses"]     += 1
                finish_game(data, bet)
                save_db(bot.db)
                e = emb(f"💥 انهار عند x{crash_point}!", f"{funny('lose')}\n😢 خسرت **${bet:,}**", C_RED)
                e.add_field(name="🪙 رصيدك", value=f"${data['balance']:,}")
                await msg.edit(embed=e, view=None)
            return
        if not cashed_out[0]:
            try: await msg.edit(embed=make_embed())
            except: pass

# ───────────────────────────────────────────────────────────────────
# تنين 🐉 (جديد!)
# ───────────────────────────────────────────────────────────────────
@bot.command(name="تنين")
async def dragon_cmd(ctx, bet: int):
    data = get_user(bot.db, str(ctx.author.id))
    err  = game_check(data, bet, 100, 20000)
    if err: await ctx.send(err); return

    e = emb(
        "🐉 لعبة التنين",
        f"رهانك: **${bet:,}**\n\nالتنين يختبئ في جهة واحدة!\nاختر **يمين** أو **يسار** — إذا اخترت صح تربح x2! 🎯\n\n⬅️ ═══════════════ ➡️",
        C_PURPLE
    )
    view = discord.ui.View()
    left  = discord.ui.Button(label="⬅️ يسار", style=discord.ButtonStyle.primary)
    right = discord.ui.Button(label="يمين ➡️", style=discord.ButtonStyle.danger)
    chosen = [False]

    async def make_choice(i: discord.Interaction, side):
        if i.user.id != ctx.author.id:
            await i.response.send_message("❌ مو لعبتك!", ephemeral=True); return
        if chosen[0]: return
        chosen[0] = True

        dragon_side = random.choice(["left", "right"])
        dragon_emoji = "⬅️" if dragon_side == "left" else "➡️"

        anim_msg = await i.response.edit_message(
            content="🐉 التنين يتحرك...",
            embed=None, view=None
        )
        for frame in ["🐉 ═══════════...", "═══🐉══════...", "══════🐉═══...", "═══════════🐉"]:
            await asyncio.sleep(0.5)
            try: await i.edit_original_response(content=frame)
            except: pass
        await asyncio.sleep(0.6)

        if side == dragon_side:
            data["balance"]      += bet
            data["total_earned"] += bet
            data["wins"]         += 1
            color = C_GREEN
            text  = f"{funny('win')}\n🎉 التنين كان في {dragon_emoji}!\nربحت **${bet*2:,}**! 🐉🔥"
            title = "🐉 وجدت التنين!"
        else:
            data["balance"]    -= bet
            data["total_lost"] += bet
            data["losses"]     += 1
            color = C_RED
            text  = f"{funny('lose')}\n😢 التنين كان في {dragon_emoji}!\nخسرت **${bet:,}**! 💀"
            title = "🐉 خسرت!"

        finish_game(data, bet)
        new_ach = check_achievements(data)
        save_db(bot.db)
        e2 = emb(title, text, color)
        e2.add_field(name="🐉 التنين كان", value=dragon_emoji,               inline=True)
        e2.add_field(name="👆 اخترت",      value="⬅️" if side=="left" else "➡️", inline=True)
        e2.add_field(name="🪙 رصيدك",     value=f"${data['balance']:,}",     inline=True)
        add_ach(e2, new_ach)
        try: await i.edit_original_response(content=None, embed=e2)
        except: pass

    async def left_cb(i):  await make_choice(i, "left")
    async def right_cb(i): await make_choice(i, "right")
    left.callback  = left_cb
    right.callback = right_cb
    view.add_item(left)
    view.add_item(right)
    await ctx.send(embed=e, view=view)

# ───────────────────────────────────────────────────────────────────
# العين 👁️ (تتحول تلقائي بعد 10 ثواني)
# ───────────────────────────────────────────────────────────────────
@bot.command(name="عين")
async def evil_eye_cmd(ctx, user: discord.User = None):
    target = user or ctx.author

    frames = [
        "😐 العين تراقب...",
        "👁️ العين تتركز...",
        "🌀 العين تشتغل...",
        "😤 العين اشتغلت!",
    ]
    msg = await ctx.send(frames[0])
    for f in frames[1:]:
        await asyncio.sleep(0.6)
        await msg.edit(content=f)
    await asyncio.sleep(0.5)

    results = [
        ("😈 العين وقعت!", f"👁️ {target.mention} أصابتهم العين! يونان فاملي تقول: ادعوا لهم! 🤲😂", C_RED),
        ("🧿 العين ما وقعت!", f"✨ {target.mention} محمي بالله! العين رجعت فاضية! 😂", C_GREEN),
        ("😱 العين قوية!", f"💀 {target.mention} العين دمّرتهم! يونان فاملي تضحك! 😂🔥", C_PURPLE),
        ("🌝 العين تعبت!", f"😂 {target.mention} العين حاولت بس ما فيه شي تأخذه، الواحد فاضي أصلاً! 💀", C_ORANGE),
    ]
    title, desc, color = random.choice(results)

    e1 = emb(title, desc, color)
    e1.set_footer(text="👁️ العين تتحول بعد 10 ثواني... | YF BANK 2026 | عائلة يونان 👑")
    await msg.edit(content=None, embed=e1)

    await asyncio.sleep(10)

    transformed = [
        ("🧿 العين انقلبت!", f"😂 العين اللي طلحت على {target.mention} رجعت على صاحبها! يونان فاملي تضحك! 🌝🔥", C_GOLD),
        ("✨ البركة نزلت!", f"🤲 بعد العين جاءت البركة على {target.mention}! يونان فاملي تقول: ماشاء الله! 💚", C_GREEN),
        ("😈 العين اشتدت!", f"💀 {target.mention} العين ما كفت! يونان فاملي تقول: ادعوا له بسرعة! 😭🤲", C_RED),
        ("🌀 العين دارت!", f"😂 {target.mention} العين دارت 3 دورات وما لقت هدف! بوت يضحك عليك! 💀🌝", C_PURPLE),
    ]
    t2, d2, c2 = random.choice(transformed)
    e2 = emb(t2, d2, c2)
    try:
        await msg.edit(embed=e2)
    except:
        pass


@bot.command(name="سوق")
async def market_cmd(ctx):
    await ctx.send(embed=build_market_embed(bot), view=MarketMenuView(ctx))

@bot.command(name="شراء")
async def buy_cmd(ctx, item_key: str, amount: int = 1):
    if item_key not in bot.market:
        await ctx.send(f"❌ ما في سلعة `{item_key}`! استخدم `-سوق`"); return
    data = get_user(bot.db, str(ctx.author.id))
    item = bot.market[item_key]
    cost = item["buy"] * amount
    if data["balance"] < cost:
        await ctx.send(embed=emb("❌ ما في فلوس!", f"تحتاج: ${cost:,}\n{funny('broke')}", C_RED)); return
    data["balance"] -= cost
    data["inventory"][item_key] = data["inventory"].get(item_key, 0) + amount
    save_db(bot.db)
    await ctx.send(embed=emb("✅ تم!", f"اشتريت **{amount}x {item['name']}** بـ **${cost:,}**\n🪙 رصيدك: ${data['balance']:,}", C_GREEN))

@bot.command(name="بيع")
async def sell_cmd(ctx, item_key: str, amount: int = 1):
    if item_key not in bot.market:
        await ctx.send(f"❌ ما في سلعة `{item_key}`!"); return
    data  = get_user(bot.db, str(ctx.author.id))
    owned = data["inventory"].get(item_key, 0)
    if owned < amount:
        await ctx.send(f"❌ عندك {owned} فقط!"); return
    item  = bot.market[item_key]
    earn  = item["sell"] * amount
    data["inventory"][item_key] -= amount
    data["balance"]      += earn
    data["total_earned"] += earn
    save_db(bot.db)
    await ctx.send(embed=emb("✅ تم البيع!", f"بعت **{amount}x {item['name']}** بـ **${earn:,}**\n🪙 رصيدك: ${data['balance']:,}", C_GREEN))

@bot.command(name="ممتلكات")
async def props_cmd(ctx):
    await ctx.send(embed=build_props_embed(), view=PropertiesView(ctx))



# ═══════════════════════════════════════════════════════════════════
# تشغيل البوت
# ═══════════════════════════════════════════════════════════════════
BANK_CHANNEL_ID = 1495452176313745511

@bot.check
async def only_bank_channel(ctx):
    if ctx.channel.id != BANK_CHANNEL_ID:
        return False
    return True

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
