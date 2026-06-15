import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from utils.db import get_user

PROFILE_BG = "DFDE05FC-39AA-42A6-875F-B319DB14C725.png"

def get_avatar_img(url, size=(415, 415)):
    r = requests.get(url, timeout=10)
    img = Image.open(BytesIO(r.content)).convert("RGBA").resize(size)

    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + size, fill=255)
    img.putalpha(mask)

    return img

def load_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "DejaVuSans.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="رصيد")
    async def profile(self, ctx, user: discord.Member = None):
        target = user or ctx.author

        data = get_user(self.bot.db, str(target.id))

        # فتح الخلفية الأصلية
        bg = Image.open(PROFILE_BG).convert("RGBA")
        draw = ImageDraw.Draw(bg)

        # تجهيز الخطوط المتوافقة مع السيرفر بحجم متناسق
        f_main = load_font(60)
        f_side = load_font(50)

        # [1] تثبيت صورة البروفايل الدائرية داخل الإطار الدائري الأخضر بالملي
        try:
            avatar = get_avatar_img(str(target.display_avatar.url), (415, 415))
            bg.paste(avatar, (295, 715), avatar)
        except Exception as e:
            print(f"Error loading avatar: {e}")

        total = data["balance"] + data["bank"]

        # [2] المربع الأول: الاسم (توسيط داخل مستطيل الاسم الأول)
        draw.text((2360, 520), str(target.display_name[:15]), font=f_main, fill="white", anchor="mm")

        # [3] المربع الثاني: الفلوس (توسيط داخل مستطيل الفلوس)
        draw.text((2360, 740), f"{total:,} $", font=f_main, fill="#ffd700", anchor="mm")

        # [4] المربع الثالث: الخسائر والفوز (توسيط الأرقام داخل مربعات الفوز والخسارة)
        draw.text((2070, 960), str(data['losses']), font=f_side, fill="#f87171", anchor="mm")
        draw.text((2650, 960), str(data['wins']), font=f_side, fill="#4ade80", anchor="mm")

        # [5] المربع الرابع: الحالة الاقتصادية (توسيط داخل مستطيل الحالة)
        if total >= 100000:
            status = "Rich"
            status_color = "#ffd700"
        elif total >= 50000:
            status = "Medium"
            status_color = "#4ade80"
        else:
            status = "Poor"
            status_color = "#f87171"

        draw.text((2360, 1180), status, font=f_main, fill=status_color, anchor="mm")

        # [6] الشريط السفلي: اللفل والـ XP (توسيط البيانات على الأطراف المخصصة لها تحت)
        lvl_text = f"Level {data['level']}"
        xp_text = f"{data['xp']:,} XP"
        
        draw.text((1950, 1545), lvl_text, font=f_side, fill="white", anchor="lm")
        draw.text((3150, 1545), xp_text, font=f_side, fill="white", anchor="rm")

        # حفظ الكرت وإرساله
        buf = BytesIO()
        bg.convert("RGB").save(buf, format="PNG")
        buf.seek(0)

        await ctx.send(file=discord.File(buf, filename="profile.png"))

async def setup(bot):
    await bot.add_cog(Images(bot))
    
