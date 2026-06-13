import discord
from discord.ext import commands
import os, asyncio

from utils.db import load_db, save_db

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents, help_command=None)
bot.db = load_db()

COGS = [
    "cogs.economy",
    "cogs.games",
    "cogs.protection",
    "cogs.social",
    "cogs.info",
    "cogs.images",
]

@bot.event
async def on_ready():
    print(f"✅ {bot.user} شغال!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ ناقص معلومة! استخدم `-مساعدة`")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ خطأ في الأمر! استخدم `-مساعدة`")
    elif isinstance(error, commands.CommandNotFound):
        pass

async def main():
    async with bot:
        for cog in COGS:
            await bot.load_extension(cog)
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("❌ ما في توكن!")
            return
        await bot.start(token)

asyncio.run(main())
