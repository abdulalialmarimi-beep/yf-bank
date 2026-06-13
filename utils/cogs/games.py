import discord, random
from discord.ext import commands
from datetime import datetime, timedelta
from typing import Optional

from config import C_GOLD, C_GREEN, C_RED, C_BLUE, COOLDOWN_MIN, COOLDOWN_MAX
from utils.db import get_user, save_db
from utils.helpers import emb, fmt, funny, add_xp, get_rank


def check_cooldown(data, game):
    cd = data["cooldowns"].get(game)
    if not cd: return None
    remaining = datetime.fromisoformat(cd) - datetime.now()
    return remaining if remaining.total_seconds() > 0 else None

def set_cooldown(data, game):
    minutes = random.randint(COOLDOWN_MIN, COOLDOWN_MAX)
    data["cooldowns"][game] = (datetime.now() + timedelta(minutes=minutes)).isoformat()
    return minutes

def cd_msg(r):
    m = int(r.total_seconds() // 60)
    s = int(r.total_seconds() % 60)
    return f"⏳ انتظر **{m}د {s}ث**!"


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="العاب")
    async def games_list(self, ctx):
        e = emb("🎮 الألعاب", color=C_GOLD)
        e.add_field(name="🎰 سلوتس",   value="`-سلوتس [مبلغ]`",         inline=False)
        e.add_field(name="🎲 نرد",      value="`-نرد [مبلغ]`",           inline=False)
        e.add_field(name="🔴 روليت",   value="`-روليت [لون] [مبلغ]`",   inline=False)
        e.add_field(name="🃏 بلاك جاك", value="`-بلاك [مبلغ]`",         inline=False)
        e.add_field(name="🦹 نهب",      value="`-نهب @شخص`",             inline=False)
        e.add_field(name="⏱️ Cooldown", value=f"عشوائي {COOLDOWN_MIN}-{COOLDOWN_MAX} دقايق", inline=False)
        await ctx.send(embed=e)

    @commands.command(name="سلوتس")
    async def slots(self, ctx, bet: int):
        data = get_user(self.bot.db, str(ctx.author.id))
        if rem := check_cooldown(data, "سلوتس"):
            await ctx.send(cd_msg(rem)); return
        if bet < 100 or bet > 100_000:
            await ctx.send("❌ الرهان بين $100 و$100,000!"); return
        if data["balance"] < bet:
            await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
        symbols = ["🍒","🍋","🍊","🍇","⭐","💎","7️⃣"]
        weights = [30,25,20,15,6,3,1]
        reels   = random.choices(symbols, weights=weights, k=3)
        result  = " | ".join(reels)
        cd      = set_cooldown(data, "سلوتس")
        if reels[0] == reels[1] == reels[2]:
            mult = 50 if reels[0] == "7️⃣" else 20 if reels[0] == "💎" else 5
            gain = int(bet * mult) - bet
            data["balance"] += gain; data["total_earned"] += gain; data["wins"] += 1; data["games_played"] += 1
            leveled, xp = add_xp(data, bet * mult)
            e = emb("🎰 فوز!", f"**{result}**\n{funny('win')}", C_GREEN)
            e.add_field(name="💰 ربحت", value=f"${gain:,}", inline=True)
        elif reels[0]==reels[1] or reels[1]==reels[2]:
            gain = int(bet * 0.5)
            data["balance"] += gain; data["games_played"] += 1
            leveled, xp = add_xp(data, gain)
            e = emb("🎰 نص فوز!", f"**{result}**", C_BLUE)
            e.add_field(name="💰 ربحت", value=f"${gain:,}", inline=True)
        else:
            data["balance"] -= bet; data["total_lost"] += bet; data["losses"] += 1; data["games_played"] += 1
            leveled, xp = add_xp(data, 0)
            e = emb("🎰 خسارة!", f"**{result}**\n{funny('lose')}", C_RED)
            e.add_field(name="💀 خسرت", value=f"${bet:,}", inline=True)
        e.add_field(name="🪙 رصيدك", value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="⏱️ انتظر", value=f"{cd} دقيقة", inline=True)
        save_db(self.bot.db)
        await ctx.send(embed=e)

    @commands.command(name="نرد")
    async def dice(self, ctx, bet: int):
        data = get_user(self.bot.db, str(ctx.author.id))
        if rem := check_cooldown(data, "نرد"):
            await ctx.send(cd_msg(rem)); return
        if bet < 100 or bet > 50_000:
            await ctx.send("❌ الرهان بين $100 و$50,000!"); return
        if data["balance"] < bet:
            await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
        player = random.randint(1,6)
        bot_   = random.randint(1,6)
        cd     = set_cooldown(data, "نرد")
        if player > bot_:
            data["balance"] += bet; data["total_earned"] += bet; data["wins"] += 1; data["games_played"] += 1
            e = emb("🎲 فوز!", f"أنت: **{player}** | البوت: **{bot_}**\n{funny('win')}", C_GREEN)
            e.add_field(name="💰 ربحت", value=f"${bet:,}", inline=True)
        elif player < bot_:
            data["balance"] -= bet; data["total_lost"] += bet; data["losses"] += 1; data["games_played"] += 1
            e = emb("🎲 خسارة!", f"أنت: **{player}** | البوت: **{bot_}**\n{funny('lose')}", C_RED)
            e.add_field(name="💀 خسرت", value=f"${bet:,}", inline=True)
        else:
            data["games_played"] += 1
            e = emb("🎲 تعادل!", f"أنت: **{player}** | البوت: **{bot_}**\n🤝", C_BLUE)
        e.add_field(name="🪙 رصيدك", value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="⏱️ انتظر", value=f"{cd} دقيقة", inline=True)
        save_db(self.bot.db)
        await ctx.send(embed=e)

    @commands.command(name="روليت")
    async def roulette(self, ctx, color: str, bet: int):
        data = get_user(self.bot.db, str(ctx.author.id))
        if rem := check_cooldown(data, "روليت"):
            await ctx.send(cd_msg(rem)); return
        if color not in ["احمر","اسود","اخضر"]:
            await ctx.send("❌ اختر: `احمر` أو `اسود` أو `اخضر`!"); return
        if bet < 100 or bet > 100_000:
            await ctx.send("❌ الرهان بين $100 و$100,000!"); return
        if data["balance"] < bet:
            await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
        spin  = random.choices(["احمر","اسود","اخضر"], weights=[47,47,6])[0]
        icons = {"احمر":"🔴","اسود":"⚫","اخضر":"🟢"}
        mults = {"احمر":2,"اسود":2,"اخضر":14}
        cd    = set_cooldown(data, "روليت")
        if spin == color:
            gain = int(bet * mults[color]) - bet
            data["balance"] += gain; data["total_earned"] += gain; data["wins"] += 1; data["games_played"] += 1
            e = emb("🎡 فوز!", f"النتيجة: {icons[spin]} **{spin}**\n{funny('win')}", C_GREEN)
            e.add_field(name="💰 ربحت", value=f"${gain:,}", inline=True)
        else:
            data["balance"] -= bet; data["total_lost"] += bet; data["losses"] += 1; data["games_played"] += 1
            e = emb("🎡 خسارة!", f"النتيجة: {icons[spin]} **{spin}**\n{funny('lose')}", C_RED)
            e.add_field(name="💀 خسرت", value=f"${bet:,}", inline=True)
        e.add_field(name="🪙 رصيدك", value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="⏱️ انتظر", value=f"{cd} دقيقة", inline=True)
        save_db(self.bot.db)
        await ctx.send(embed=e)

    @commands.command(name="بلاك")
    async def blackjack(self, ctx, bet: int):
        data = get_user(self.bot.db, str(ctx.author.id))
        if rem := check_cooldown(data, "بلاك"):
            await ctx.send(cd_msg(rem)); return
        if bet < 100 or bet > 100_000:
            await ctx.send("❌ الرهان بين $100 و$100,000!"); return
        if data["balance"] < bet:
            await ctx.send(embed=emb("❌ ما في فلوس!", funny("broke"), C_RED)); return
        def card(): return random.choice(["A","2","3","4","5","6","7","8","9","10","J","Q","K"])
        def value(hand):
            total, aces = 0, 0
            for c in hand:
                if c in ["J","Q","K"]: total += 10
                elif c == "A": total += 11; aces += 1
                else: total += int(c)
            while total > 21 and aces: total -= 10; aces -= 1
            return total
        ph = [card(), card()]; bh = [card(), card()]
        pv = value(ph); bv = value(bh)
        while bv < 17: bh.append(card()); bv = value(bh)
        cd = set_cooldown(data, "بلاك")
        p_hand = " ".join(ph); b_hand = " ".join(bh)
        if pv > 21:
            data["balance"] -= bet; data["total_lost"] += bet; data["losses"] += 1; data["games_played"] += 1
            e = emb("🃏 خسارة!", f"يدك: {p_hand} ({pv}) 💥\n{funny('lose')}", C_RED)
            e.add_field(name="💀 خسرت", value=f"${bet:,}", inline=True)
        elif bv > 21 or pv > bv:
            data["balance"] += bet; data["total_earned"] += bet; data["wins"] += 1; data["games_played"] += 1
            e = emb("🃏 فوز!", f"يدك: {p_hand} ({pv})\nالبوت: {b_hand} ({bv})\n{funny('win')}", C_GREEN)
            e.add_field(name="💰 ربحت", value=f"${bet:,}", inline=True)
        elif pv == bv:
            data["games_played"] += 1
            e = emb("🃏 تعادل!", f"يدك: {p_hand} ({pv})\nالبوت: {b_hand} ({bv})\n🤝", C_BLUE)
        else:
            data["balance"] -= bet; data["total_lost"] += bet; data["losses"] += 1; data["games_played"] += 1
            e = emb("🃏 خسارة!", f"يدك: {p_hand} ({pv})\nالبوت: {b_hand} ({bv})\n{funny('lose')}", C_RED)
            e.add_field(name="💀 خسرت", value=f"${bet:,}", inline=True)
        e.add_field(name="🪙 رصيدك", value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="⏱️ انتظر", value=f"{cd} دقيقة", inline=True)
        save_db(self.bot.db)
        await ctx.send(embed=e)

    @commands.command(name="نهب")
    async def rob(self, ctx, user: discord.Member):
        if user.id == ctx.author.id:
            await ctx.send("❌ ما تقدر تسرق نفسك!"); return
        data   = get_user(self.bot.db, str(ctx.author.id))
        target = get_user(self.bot.db, str(user.id))
        if rem := check_cooldown(data, "نهب"):
            await ctx.send(cd_msg(rem)); return
        if target["balance"] < 500:
            await ctx.send(embed=emb("😂 فقير!", f"{user.display_name} ما عنده شيء!", C_RED)); return
        if target["protection_until"]:
            if datetime.fromisoformat(target["protection_until"]) > datetime.now():
                await ctx.send(embed=emb("🛡️ محمي!", f"{user.display_name} عنده حماية!", C_BLUE)); return
        cd = set_cooldown(data, "نهب")
        if random.random() < 0.45:
            amount = random.randint(int(target["balance"]*0.1), int(target["balance"]*0.3))
            target["balance"] -= amount; data["balance"] += amount
            data["rob_success"] = data.get("rob_success",0) + 1
            e = emb("🦹 نهب ناجح!", f"{funny('rob_success')}\nسرقت **${amount:,}** من {user.display_name}!", C_GREEN)
            e.add_field(name="💰 ربحت", value=f"${amount:,}", inline=True)
        else:
            fine = random.randint(500,2000)
            data["balance"] = max(0, data["balance"] - fine)
            e = emb("👮 انكشفت!", f"{funny('rob_fail')}\nغرامة **${fine:,}**!", C_RED)
            e.add_field(name="💀 الغرامة", value=f"${fine:,}", inline=True)
        e.add_field(name="🪙 رصيدك", value=f"${fmt(data['balance'])}", inline=True)
        e.add_field(name="⏱️ انتظر", value=f"{cd} دقيقة", inline=True)
        save_db(self.bot.db)
        await ctx.send(embed=e)


async def setup(bot):
    await bot.add_cog(Games(bot))
