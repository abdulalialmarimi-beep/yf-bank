import discord
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# مكتبات لضبط وتعديل اتجاه النصوص العربية ومنع العوج
import arabic_reshaper
from bidi.algorithm import get_display

from utils.db import get_user

PROFILE_BG = "DFDE05FC-39AA-42A6-875F-B319DB14C725.png"

def get_avatar_img(url, size=(520, 520)):
    r = requests.get(url, timeout=10)
    img = Image.open(BytesIO(r.content)).convert("RGBA").resize(size)

    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + size, fill=255)
    img.putalpha(mask)

    return img

def load_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 
        "arial.ttf"
    ]
    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

# دالة لتهيئة النص العربي ليظهر مشبك وصحيح
def format_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="رصيد")
    async def profile(self, ctx, user: discord.Member = None):
        target = user or ctx.author

        data = get_user(self.bot.db, str(target.id))

        # فتح الخلفية بحجمها الأصلي الفخم 4096x1718
        bg = Image.open(PROFILE_BG).convert("RGBA")
        draw = ImageDraw.Draw(bg)

        # حجم الخطوط المناسب لأبعاد الصورة الضخمة
        f_main = load_font(75)
        f_side = load_font(65)

        # [1] صورة البروفايل الدائرية على اليسار
        try:
            avatar = get_avatar_img(str(target.display_avatar.url), (530, 530))
            bg.paste(avatar, (460, 440), avatar)
        except Exception as e:
            print(f"Error loading avatar: {e}")

        # حساب مجموع الأموال
        total = data["balance"] + data["bank"]

        # [2] المربع الأول فوق على اليمين: الاسم
        clean_name = format_arabic(target.display_name[:15])
        draw.text((2350, 465), clean_name, font=f_main, fill="white", anchor="mm")

        # [3] المربع الثاني تحت الاسم: الفلوس
        money_text = format_arabic(f"رصيد: {total:,} $")
        draw.text((2350, 680), money_text, font=f_main, fill="#ffd700", anchor="mm")

        # [4] المربع الثالث: الخسائر على اليسار، والفوز على اليمين
        losses_text = format_arabic(f"الخسائر: {data['losses']}")
        wins_text = format_arabic(f"الفوز: {data['wins']}")
        
        draw.text((2050, 895), losses_text, font=f_side, fill="#f87171", anchor="mm")  # يسار المربع
        draw.text((2650, 895), wins_text, font=f_side, fill="#4ade80", anchor="mm")    # يمين المربع

        # [5] المربع الرابع: الحالة الاقتصادية
        if total >= 100000:
            status = "غني"
            status_color = "#ffd700"
        elif total >= 50000:
            status = "متوسط"
            status_color = "#4ade80"
        else:
            status = "فقير"
            status_color = "#f87171"

        draw.text((2350, 1110), format_arabic(status), font=f_main, fill=status_color, anchor="mm")

        # [6] المربع السفلي الطويل: اللفل على اليسار، والـ XP على اليمين
        lvl_text = format_arabic(f"Level {data['level']}")
        xp_text = format_arabic(f"{data['xp']:,} XP")
        
        # هنا تم تصليح الخطأ وحذف الـ fill المكرر نهائياً
        draw.text((2000, 1530), lvl_text, font=f_side, fill="white", anchor="lm")
        draw.text((3100, 1530), xp_text, font=f_side, fill="white", anchor="rm")

        # حفظ وإرسال الصورة
        buf = BytesIO()
        bg.convert("RGB").save(buf, format="PNG")
        buf.seek(0)

        await ctx.send(file=discord.File(buf, filename="profile.png"))

async def setup(bot):
    await bot.add_cog(Images(bot))
    
