import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from utils.db import get_user

PROFILE_BG = "DFDE05FC-39AA-42A6-875F-B319DB14C725.png"


def get_avatar_img(url, size=(120, 120)):
    r = requests.get(url, timeout=10)
    img = Image.open(BytesIO(r.content)).convert("RGBA").resize(size)

    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + size, fill=255)
    img.putalpha(mask)

    return img


def load_font(size):
    try:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            size
        )
    except:
        return ImageFont.load_default()


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="رصيد")
    async def profile(self, ctx, user: discord.Member = None):
        target = user or ctx.author

        data = get_user(self.bot.db, str(target.id))

        bg = Image.open(PROFILE_BG).convert("RGBA")
        draw = ImageDraw.Draw(bg)

        # الخطوط
        f_name = load_font(60)
        f_money = load_font(55)
        f_stats = load_font(50)
        f_level = load_font(50)

        # صورة العضو
        try:
            avatar = get_avatar_img(
                str(target.display_avatar.url),
                (420, 420)
            )

            bg.paste(
                avatar,
                (520, 650),
                avatar
            )
        except:
            pass

        # مجموع الأموال
        total = data["balance"] + data["bank"]

        # الاسم
        draw.text(
            (950, 660),
            target.display_name[:18],
            font=f_name,
            fill="white"
        )

        # الفلوس
        draw.text(
            (950, 820),
            f"${total:,}",
            font=f_money,
            fill="#d4a843"
        )

        # الخسائر
        draw.text(
            (1120, 1010),
            str(data["losses"]),
            font=f_stats,
            fill="#f87171"
        )

        # الفوز
        draw.text(
            (1540, 1010),
            str(data["wins"]),
            font=f_stats,
            fill="#4ade80"
        )

        # الحالة
        if total >= 100000:
            status = "غني"
            status_color = "#ffd700"
        elif total >= 50000:
            status = "متوسط"
            status_color = "#4ade80"
        else:
            status = "فقير"
            status_color = "#f87171"

        draw.text(
            (950, 1180),
            status,
            font=f_stats,
            fill=status_color
        )

        # المستوى
        draw.text(
            (950, 1450),
            f"Level {data['level']}",
            font=f_level,
            fill="white"
        )

        # XP
        draw.text(
            (1500, 1450),
            f"{data['xp']:,} XP",
            font=f_level,
            fill="white"
        )

        buf = BytesIO()
        bg.convert("RGB").save(buf, format="PNG")
        buf.seek(0)

        await ctx.send(
            file=discord.File(
                buf,
                filename="profile.png"
            )
        )


async def setup(bot):
    await bot.add_cog(Images(bot))
