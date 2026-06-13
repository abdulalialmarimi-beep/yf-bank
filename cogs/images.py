import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from utils.db import get_user, save_db
from utils.helpers import fmt, get_rank

PROFILE_BG = "PROFILE_BG.png"
TOP_BG     = "IMG-20260613-WA0002.jpg"


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
        f_big  = load_font(90)
        f_med  = load_font(75)
        f_small= load_font(62)

        # ── 1: صورة العضو ──
        try:
            avatar = get_avatar_img(str(target.display_avatar.url), (170, 170))
            bg.paste(avatar, (175, 130), avatar)
        except:
            pass

        # ── 2: اسم العضو ──
        draw.text((200, 540), target.display_name[:16], font=f_med, fill="#d4a843")

        # ── 3: الرصيد الكلي (balance + bank) ──
        total = data['balance'] + data['bank']
        draw.text((570, 245), f"${total:,}", font=f_big, fill="white")

        # ── 4: الممتلكات ──
        draw.text((630, 360), str(sum(data["inventory"].values())), font=f_med, fill="white")

        # ── 5: الانتصارات ──
        draw.text((590, 460), str(data["wins"]), font=f_med, fill="#4ade80")

        # ── 6: الخسائر ──
        draw.text((798, 445), str(data["losses"]), font=f_med, fill="#f87171")

        # ── 7: عدد مرات السرقة عليه ──
        draw.text((590, 565), str(data.get("stolen_count", 0)), font=f_med, fill="white")

        # ── 8: ساعات الحماية ──
        draw.text((1060, 565), str(data.get("shield_hours", 0)), font=f_small, fill="#4ade80")

        # ── 9: كم مرة سرق هو ──
        draw.text((1230, 565), str(data.get("steal_count", 0)), font=f_small, fill="#f87171")

        # ── 10: Level + XP ──
        draw.text((670, 778),  f"Level {data['level']}", font=f_med, fill="white")
        draw.text((1050, 778), f"{data['xp']}/{data['level']*1000} XP", font=f_med, fill="white")

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
        font = load_font(32)

        rows = [
            {"av": (95,462),  "nm": (185,472),  "mn": (710,472)},
            {"av": (95,612),  "nm": (185,622),  "mn": (710,622)},
            {"av": (95,762),  "nm": (185,772),  "mn": (710,772)},
            {"av": (95,912),  "nm": (185,922),  "mn": (710,922)},
            {"av": (95,1062), "nm": (185,1072), "mn": (710,1072)},
        ]

        for i, (member, total) in enumerate(users[:5]):
            try:
                av = get_avatar_img(str(member.display_avatar.url), (80,80))
                bg.paste(av, rows[i]["av"], av)
            except:
                pass
            draw.text(rows[i]["nm"], member.display_name[:16], font=font, fill="white")
            draw.text(rows[i]["mn"], f"${total:,}",            font=font, fill="#d4a843")

        buf = BytesIO()
        bg.convert("RGB").save(buf, format="PNG")
        buf.seek(0)
        await ctx.send(file=discord.File(buf, "top.png"))


async def setup(bot):
    await bot.add_cog(Images(bot))
        
