import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from utils.db import get_user, save_db
from utils.helpers import fmt, get_rank

PROFILE_BG = "IMG-20260613-WA0001.jpg"
TOP_BG     = "IMG-20260613-WA0002.jpg"


def get_avatar(url):
    r = requests.get(url)
    return Image.open(BytesIO(r.content)).convert("RGBA")

def circle_avatar(img, size=(120,120)):
    img = img.resize(size)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0,0)+size, fill=255)
    img.putalpha(mask)
    return img


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="رصيد")
    async def profile(self, ctx, user: discord.Member = None):
        target = user or ctx.author
        data   = get_user(self.bot.db, str(target.id))

        bg   = Image.open(PROFILE_BG).convert("RGBA")
        draw = ImageDraw.Draw(bg)

        try:
            font_big   = ImageFont.truetype("arial.ttf", 36)
            font_med   = ImageFont.truetype("arial.ttf", 28)
            font_small = ImageFont.truetype("arial.ttf", 22)
        except:
            font_big   = ImageFont.load_default()
            font_med   = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # صورة البروفايل
        avatar_url = str(target.display_avatar.url)
        avatar     = circle_avatar(get_avatar(avatar_url))
        bg.paste(avatar, (60, 120), avatar)

        # الاسم
        draw.text((60, 250), target.display_name, font=font_med, fill="#d4a843")

        # الرصيد
        total = data["balance"] + data["bank"]
        draw.text((490, 165), f"${fmt(total)}", font=font_big, fill="white")

        # المستوى
        draw.text((490, 245), get_rank(data["level"]), font=font_med, fill="white")

        # الممتلكات والألعاب
        draw.text((490, 325), str(sum(data["inventory"].values())), font=font_med, fill="white")
        draw.text((680, 325), str(data["games_played"]),            font=font_med, fill="white")

        # الأرباح والخسائر
        draw.text((870, 390), f"${fmt(data['total_earned'])}", font=font_med, fill="#4ade80")
        draw.text((870, 460), f"${fmt(data['total_lost'])}",   font=font_med, fill="#f87171")

        # XP
        xp_need = data["level"] * 1000
        draw.text((490, 580), f"Level {data['level']}", font=font_med, fill="white")
        draw.text((900, 580), f"{data['xp']}/{xp_need} XP", font=font_med, fill="white")

        buf = BytesIO()
        bg.save(buf, format="PNG")
        buf.seek(0)
        await ctx.send(file=discord.File(buf, "profile.png"))

    @commands.command(name="مطنوخين")
    async def top(self, ctx):
        users = [
            (ctx.guild.get_member(int(uid)), d["balance"] + d["bank"])
            for uid, d in self.bot.db.items()
            if ctx.guild.get_member(int(uid))
        ]
        users.sort(key=lambda x: x[1], reverse=True)

        bg   = Image.open(TOP_BG).convert("RGBA")
        draw = ImageDraw.Draw(bg)

        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()

        positions = [195, 305, 415, 525, 635]

        for i, (member, total) in enumerate(users[:5]):
            y = positions[i]

            # صورة البروفايل
            avatar_url = str(member.display_avatar.url)
            avatar     = circle_avatar(get_avatar(avatar_url), (70,70))
            bg.paste(avatar, (155, y-30), avatar)

            # الاسم
            draw.text((240, y-10), member.display_name, font=font, fill="white")

            # الرصيد
            draw.text((700, y-10), f"${fmt(total)}", font=font, fill="#d4a843")

        buf = BytesIO()
        bg.save(buf, format="PNG")
        buf.seek(0)
        await ctx.send(file=discord.File(buf, "top.png"))


async def setup(bot):
    await bot.add_cog(Images(bot))
