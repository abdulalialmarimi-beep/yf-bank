import discord
from discord.ext import commands
from datetime import datetime, timedelta
from typing import Optional

from config import C_GOLD, C_GREEN, C_RED, C_PURPLE, DAILY_BASE, DAILY_STREAK, DAILY_MAX, SHOP_ITEMS
from utils.db import get_user, save_db
from utils.helpers import emb, fmt, funny, get_rank, add_xp, bar


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="رصيد")
    async def balance(self, ctx, user: Optional[discord.Member] = None):
        target = user or ctx.author
        data   = get_user(self.bot.db, str(target.id))
        total  = data["balance"] + data["bank"]
        xp_need = data["level"] * 1000
        xp_cur  = data["xp"] % xp_need if xp_need else 0
        e = emb(f"💳 رصيد {target.display_name}", color=C_GOLD)
        e.add_field(name="💰 الإجمالي", value=f"**${fmt(total)}**", inline=False)
        e.add_field(name="🪙 اليد",     value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="🏛️ البنك",   value=f"${fmt(data['bank'])}",    inline=True)
        e.add_field(name="⚡ المستوى",  value=f"{get_rank(data['level'])} | Lv{data['level']}", inline=False)
        e.add_field(name="📊 XP",       value=f"`{bar(xp_cur, xp_need)}` {xp_cur}/{xp_need}", inline=False)
        e.add_field(name="🎮 ألعاب",    value=str(data["games_played"]), inline=True)
        e.add_field(name="🏆 فوز",      value=str(data["wins"]),         inline=True)
        e.add_field(name="💀 خسارة",    value=str(data["losses"]),       inline=True)
        await ctx.send(embed=e)

    @commands.command(name="يومي")
    async def daily(self, ctx):
        data = get_user(self.bot.db, str(ctx.author.id))
        now  = datetime.now()
        if data["last_daily"]:
            diff = now - datetime.fromisoformat(data["last_daily"])
            if diff < timedelta(hours=24):
                rem = timedelta(hours=24) - diff
                h   = int(rem.total_seconds() // 3600)
                m   = int((rem.total_seconds() % 3600) // 60)
                await ctx.send(embed=emb("⏳ بكره!", f"ارجع بعد **{h}س {m}د**", C_RED))
                return
            data["streak"] = 1 if diff > timedelta(hours=48) else data["streak"] + 1
        else:
            data["streak"] = 1
        streak_bonus = min(data["streak"] * DAILY_STREAK, DAILY_MAX)
        total        = DAILY_BASE + streak_bonus
        data["balance"]      += total
        data["total_earned"] += total
        data["last_daily"]    = now.isoformat()
        leveled, xp = add_xp(data, total)
        save_db(self.bot.db)
        e = emb("🎁 مكافأة اليوم!", color=C_GREEN)
        e.add_field(name="💰 أساسية",  value=f"${DAILY_BASE:,}", inline=True)
        e.add_field(name="🔥 سلسلة",  value=f"+${streak_bonus:,} (x{data['streak']})", inline=True)
        e.add_field(name="💎 المجموع", value=f"**${total:,}**", inline=False)
        e.add_field(name="⚡ XP",      value=f"+{xp} XP", inline=True)
        e.add_field(name="🪙 رصيدك",  value=f"${fmt(data['balance'])}", inline=True)
        if leveled:
            e.add_field(name="🆙 مستوى جديد!", value=f"**{get_rank(data['level'])}** Lv{data['level']} 🎉", inline=False)
        await ctx.send(embed=e)

    @commands.command(name="ايداع")
    async def deposit(self, ctx, amount: int):
        data = get_user(self.bot.db, str(ctx.author.id))
        if amount < 1:
            await ctx.send("❌ أدخل مبلغ صحيح!"); return
        if data["balance"] < amount:
            await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
        data["balance"] -= amount
        data["bank"]    += amount
        save_db(self.bot.db)
        e = emb("🏛️ إيداع ناجح!", f"أودعت **${amount:,}**", C_GREEN)
        e.add_field(name="🪙 اليد",   value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="🏛️ البنك", value=f"${fmt(data['bank'])}",    inline=True)
        await ctx.send(embed=e)

    @commands.command(name="سحب")
    async def withdraw(self, ctx, amount: int):
        data = get_user(self.bot.db, str(ctx.author.id))
        if amount < 1:
            await ctx.send("❌ أدخل مبلغ صحيح!"); return
        if data["bank"] < amount:
            await ctx.send(embed=emb("❌ البنك ما يكفي!", funny("broke"), C_RED)); return
        data["bank"]    -= amount
        data["balance"] += amount
        save_db(self.bot.db)
        e = emb("🏛️ سحب ناجح!", f"سحبت **${amount:,}**", C_GREEN)
        e.add_field(name="🪙 اليد",   value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="🏛️ البنك", value=f"${fmt(data['bank'])}",    inline=True)
        await ctx.send(embed=e)

    @commands.command(name="تحويل")
    async def transfer(self, ctx, user: discord.Member, amount: int):
        if user.id == ctx.author.id:
            await ctx.send("❌ ما تقدر تحول لنفسك!"); return
        data   = get_user(self.bot.db, str(ctx.author.id))
        target = get_user(self.bot.db, str(user.id))
        if data["balance"] < amount:
            await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
        data["balance"]   -= amount
        target["balance"] += amount
        save_db(self.bot.db)
        await ctx.send(embed=emb("💸 تحويل ناجح!", f"{ctx.author.mention} ➡️ {user.mention}\n**${amount:,}**", C_GREEN))

    @commands.command(name="هدية")
    async def gift(self, ctx, user: discord.Member, amount: int):
        if user.id == ctx.author.id:
            await ctx.send("❌ ما تقدر تهدي نفسك!"); return
        data   = get_user(self.bot.db, str(ctx.author.id))
        target = get_user(self.bot.db, str(user.id))
        if data["balance"] < amount:
            await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
        data["balance"]   -= amount
        target["balance"] += amount
        save_db(self.bot.db)
        await ctx.send(embed=emb("🎁 هدية!", f"{ctx.author.mention} أهدى {user.mention}\n**${amount:,}** 🎁", C_GREEN))

    @commands.command(name="مطنوخين")
    async def top(self, ctx):
        users = [
            (ctx.guild.get_member(int(uid)), d["balance"] + d["bank"], d["level"])
            for uid, d in self.bot.db.items()
            if ctx.guild.get_member(int(uid))
        ]
        users.sort(key=lambda x: x[1], reverse=True)
        medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e = emb("🏆 قائمة المطنوخين", "أغنى أعضاء عائلة يونان 👑", C_GOLD)
        for i, (member, total, lvl) in enumerate(users[:10]):
            e.add_field(name=f"{medals[i]} {member.display_name}", value=f"💰 ${fmt(total)} | {get_rank(lvl)}", inline=False)
        await ctx.send(embed=e)

    @commands.command(name="شراء")
    async def shop(self, ctx, item: Optional[str] = None, amount: int = 1):
        data = get_user(self.bot.db, str(ctx.author.id))
        if not item:
            e = emb("🛒 السوق", "اكتب `-شراء [اسم الشيء]` للشراء", C_GOLD)
            for name, info in SHOP_ITEMS.items():
                e.add_field(name=f"{info['icon']} {name}", value=f"${info['price']:,}\n{info['desc']}", inline=True)
            await ctx.send(embed=e); return
        if item not in SHOP_ITEMS:
            await ctx.send(f"❌ ما في شيء اسمه `{item}`!"); return
        info  = SHOP_ITEMS[item]
        total = info["price"] * amount
        if data["balance"] < total:
            await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
        data["balance"]         -= total
        data["inventory"][item]  = data["inventory"].get(item, 0) + amount
        save_db(self.bot.db)
        e = emb("✅ تم الشراء!", color=C_GREEN)
        e.add_field(name=f"{info['icon']} {item}", value=f"x{amount} — ${total:,}", inline=False)
        e.add_field(name="🪙 رصيدك", value=f"${fmt(data['balance'])}", inline=True)
        await ctx.send(embed=e)

    @commands.command(name="مخزون")
    async def inventory(self, ctx, user: Optional[discord.Member] = None):
        target = user or ctx.author
        data   = get_user(self.bot.db, str(target.id))
        inv    = {k: v for k, v in data["inventory"].items() if v > 0}
        e = emb(f"🗄️ مخزون {target.display_name}", color=C_PURPLE)
        if not inv:
            e.description = "المخزون فاضي! اشتري من `-شراء`"
        else:
            for name, qty in inv.items():
                info = SHOP_ITEMS.get(name, {})
                e.add_field(name=f"{info.get('icon','📦')} {name}", value=f"x{qty}", inline=True)
        await ctx.send(embed=e)


async def setup(bot):
    await bot.add_cog(Economy(bot))
