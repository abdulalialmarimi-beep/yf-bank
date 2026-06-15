import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from utils.db import get_user, save_db
from utils.helpers import fmt, get_rank

PROFILE_BG = "DFDE05FC-39AA-42A6-875F-B319DB14C725.png"
# الصورة الأفقية الجديدة
TOP_BG     = "TOP_BG.png"       # صورة التوب الجديدة


def get_avatar_img(url, size=(120,120)):
    r   = requests.get(url, timeout=10)
    img = Image.open(BytesIO(r.content)).convert("RGBA").resize(size)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0,0)+size, fill=255)
    img.putalpha(mask)
    return img

def load_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="رصيد")
    async def profile(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        data   = get_user(self.bot.db, str(target.id))
        bg     = Image.open(PROFILE_BG).convert("RGBA")
        draw   = ImageDraw.Draw(bg)
        
        f_name   = load_font(90)
        f_money  = load_font(80)
        f_stats  = load_font(70)
        f_level  = load_font(75)

        # ── 1: صورة العضو (دائرة كبيرة على اليسار) ──
        try:
            avatar = get_avatar_img(str(target.display_avatar.url), (600, 600))
            bg.paste(avatar, (100, 350), avatar)
        except:
            pass

        # ── 2: اسم العضو ──
        draw.text((950, 280), target.display_name[:18], font=f_name, fill="white")

        # ── 3: الفلوس ──
        total = data['balance'] + data['bank']
        draw.text((950, 480), f"${total:,}", font=f_money, fill="#d4a843")

        # ── 4: الخسائر ──
        draw.text((950, 680), str(data["losses"]), font=f_stats, fill="#f87171")

        # ── 5: الانتصارات ──
        draw.text((1450, 680), str(data["wins"]), font=f_stats, fill="#4ade80")

        # ── 6: الحالة المالية ──
        total_money = data['balance'] + data['bank']
        if total_money >= 100000:
            status = "غني"
            status_color = "#ffd700"
        elif total_money >= 50000:
            status = "متوسط"
            status_color = "#4ade80"
        else:
            status = "فقير"
            status_color = "#f87171"
        
        draw.text((950, 880), status, font=f_stats, fill=status_color)

        # ── 7: Level ──
        draw.text((950, 1280), f"Level {data['level']}", font=f_level, fill="white")

        # ── 8: XP ──
        draw.text((1450, 1280), f"{data['xp']:,} XP", font=f_level, fill="white")

        buf = BytesIO()
        bg.convert("RGB").save(buf, format="PNG")
        buf.seek(0)
        await ctx.send(file=discord.File(buf, "profile.png"))

    @commands.command(name="مطنوخين")
    async def top(self, ctx):
        users = sorted([
            (ctx.guild.get_member(int(uid)), d["balance"] + d["bank"])
            for uid, d in self.bot.db.items()
            if ctx.guild.get_member(int(uid))
        ], key=lambda x: x[1], reverse=True)

        bg   = Image.open(TOP_BG).convert("RGBA")
        draw = ImageDraw.Draw(bg)
        font = load_font(55)
        f_num = load_font(40)

        # إحداثيات التوب الجديدة (للتصميم العمودي بـ 5 صفوف)
        rows = [
            {"rank": (120, 520),  "av": (220, 480),  "nm": (380, 500),  "mn": (750, 500)},
            {"rank": (120, 720),  "av": (220, 680),  "nm": (380, 700),  "mn": (750, 700)},
            {"rank": (120, 920),  "av": (220, 880),  "nm": (380, 900),  "mn": (750, 900)},
            {"rank": (120, 1120), "av": (220, 1080), "nm": (380, 1100), "mn": (750, 1100)},
            {"rank": (120, 1320), "av": (220, 1280), "nm": (380, 1300), "mn": (750, 1300)},
        ]

        for i, (member, total) in enumerate(users[:5]):
            # رقم الترتيب
            draw.text(rows[i]["rank"], f"#{i+1}", font=f_num, fill="#d4a843")
            
            try:
                av = get_avatar_img(str(member.display_avatar.url), (100, 100))
                bg.paste(av, rows[i]["av"], av)
            except:
                pass
            
            draw.text(rows[i]["nm"], member.display_name[:16], font=font, fill="white")
            draw.text(rows[i]["mn"], f"${total:,}", font=font, fill="#d4a843")

        buf = BytesIO()
        bg.convert("RGB").save(buf, format="PNG")
        buf.seek(0)
        await ctx.send(file=discord.File(buf, "top.png"))


async def setup(bot):
    await bot.add_cog(Images(bot))
    
