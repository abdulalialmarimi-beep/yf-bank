import discord
from discord.ext import commands
from datetime import datetime

from config import C_GOLD, C_GREEN, C_RED
from utils.db import get_user, save_db
from utils.helpers import emb, fmt

C_PINK = 0xff69b4

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="زواج")
    async def marry(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            await ctx.send(embed=emb("🪞 نرجسي!", "تتزوج نفسك؟", C_RED)); return
        if user.bot:
            await ctx.send(embed=emb("🤖 بوت!", "ما تقدر تتزوج بوت!", C_RED)); return
        data   = get_user(self.bot.db, str(ctx.author.id))
        target = get_user(self.bot.db, str(user.id))
        if data["married_to"]:
            await ctx.send(embed=emb("💍 متزوج!", "طلّق أول!", C_RED)); return
        if target["married_to"]:
            await ctx.send(embed=emb("💔 مرفوض!", f"{user.display_name} متزوج!", C_RED)); return
        e = emb("💍 طلب زواج!", f"{ctx.author.mention} يطلب يد {user.mention}!\n{user.mention} رد بـ `نعم` أو `لا` خلال 60 ثانية", C_PINK)
        await ctx.send(embed=e)
        def check(m):
            return m.author.id == user.id and m.channel.id == ctx.channel.id and m.content in ["نعم","لا","yes","no"]
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
        except:
            await ctx.send(embed=emb("⏰ انتهى الوقت!", f"{user.display_name} ما رد!", C_RED)); return
        if msg.content in ["لا","no"]:
            await ctx.send(embed=emb("💔 رُفضت!", f"{user.display_name} رفض!", C_RED)); return
        data["married_to"]   = str(user.id)
        target["married_to"] = str(ctx.author.id)
        save_db(self.bot.db)
        await ctx.send(embed=emb("💍 مبروك! 🎊", f"**{ctx.author.display_name}** 💍 **{user.display_name}**\nيونان فاملي تهنيكم! 🎉", C_PINK))

    @commands.command(name="طلاق")
    async def divorce(self, ctx):
        data = get_user(self.bot.db, str(ctx.author.id))
        if not data["married_to"]:
            await ctx.send(embed=emb("❓ مو متزوج!", "وش بتطلق؟", C_RED)); return
        partner_id = data["married_to"]
        partner    = self.bot.get_user(int(partner_id))
        p_data     = get_user(self.bot.db, partner_id)
        data["married_to"]   = None
        p_data["married_to"] = None
        save_db(self.bot.db)
        name = partner.display_name if partner else "المجهول"
        await ctx.send(embed=emb("💔 طلاق!", f"**{ctx.author.display_name}** طلّق **{name}** 🌝", C_RED))

    @commands.command(name="زوجي")
    async def partner(self, ctx):
        data = get_user(self.bot.db, str(ctx.author.id))
        if not data["married_to"]:
            await ctx.send(embed=emb("💔 عزب!", "استخدم `-زواج @شخص`", C_RED)); return
        partner = self.bot.get_user(int(data["married_to"]))
        name    = partner.display_name if partner else "مجهول"
        await ctx.send(embed=emb("💍 زوجك", f"**{ctx.author.display_name}** 💍 **{name}**", C_PINK))

async def setup(bot):
    await bot.add_cog(Social(bot))
