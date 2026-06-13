import discord
from discord.ext import commands
from config import C_GOLD

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="مساعدة")
    async def help(self, ctx):
        e = discord.Embed(title="📖 قائمة الأوامر — YF BANK", color=C_GOLD)
        e.add_field(name="💰 الاقتصاد", value="`-رصيد` `-يومي` `-ايداع` `-سحب` `-تحويل` `-هدية` `-مطنوخين` `-شراء` `-مخزون`", inline=False)
        e.add_field(name="🎮 الألعاب", value="`-العاب` `-سلوتس` `-نرد` `-روليت` `-بلاك` `-نهب`", inline=False)
        e.add_field(name="🛡️ الحماية", value="`-حماية` `-حماية [ساعات]`", inline=False)
        e.add_field(name="💍 الاجتماعي", value="`-زواج @شخص` `-طلاق` `-زوجي`", inline=False)
        e.set_footer(text="🏦 YF BANK | عائلة يونان 👑")
        await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(Info(bot))
