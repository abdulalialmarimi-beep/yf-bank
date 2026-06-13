import discord
from discord.ext import commands
from datetime import datetime, timedelta

from config import C_GOLD, C_GREEN, C_RED, C_BLUE, PROTECTION_PRICE_PER_HOUR
from utils.db import get_user, save_db
from utils.helpers import emb, fmt, funny


class Protection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="حماية")
    async def protection(self, ctx, hours: int = None):
        data = get_user(self.bot.db, str(ctx.author.id))
        if hours is None:
            if data["protection_until"]:
                prot = datetime.fromisoformat(data["protection_until"])
                if prot > datetime.now():
                    remaining = prot - datetime.now()
                    h = int(remaining.total_seconds() // 3600)
                    m = int((remaining.total_seconds() % 3600) // 60)
                    e = emb("🛡️ حمايتك", f"محمي لمدة **{h}س {m}د** 🛡️", C_BLUE)
                    e.add_field(name="⏰ تنتهي", value=prot.strftime("%Y-%m-%d %H:%M"), inline=False)
                    await ctx.send(embed=e); return
            e = emb("🛡️ الحماية", f"**${PROTECTION_PRICE_PER_HOUR:,}/ساعة**\n`-حماية [ساعات]`", C_GOLD)
            e.add_field(name="مثال", value="`-حماية 5` = $5,000", inline=False)
            await ctx.send(embed=e); return
        if hours < 1:
            await ctx.send("❌ أقل ساعة واحدة!"); return
        cost = hours * PROTECTION_PRICE_PER_HOUR
        if data["balance"] < cost:
            await ctx.send(embed=emb("❌ ما في فلوس!", f"تحتاج **${cost:,}**\n{funny('broke')}", C_RED)); return
        data["balance"] -= cost
        base = datetime.fromisoformat(data["protection_until"]) if data["protection_until"] and datetime.fromisoformat(data["protection_until"]) > datetime.now() else datetime.now()
        data["protection_until"] = (base + timedelta(hours=hours)).isoformat()
        save_db(self.bot.db)
        end_time = datetime.fromisoformat(data["protection_until"])
        e = emb("🛡️ تم التفعيل!", f"محمي لـ **{hours} ساعة** 🛡️", C_GREEN)
        e.add_field(name="💰 الدفع",  value=f"${cost:,}", inline=True)
        e.add_field(name="🪙 رصيدك", value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="⏰ تنتهي",  value=end_time.strftime("%Y-%m-%d %H:%M"), inline=False)
        await ctx.send(embed=e)


async def setup(bot):
    await bot.add_cog(Protection(bot))
