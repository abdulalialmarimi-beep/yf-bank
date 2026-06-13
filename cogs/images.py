IMAGES = {
    "slots_win":     "",
    "slots_jackpot": "",
    "slots_lose":    "",
    "daily":         "",
    "marry":         "",
    "divorce":       "",
    "rob_success":   "",
    "rob_fail":      "",
    "protection":    "",
    "top_bg":        "",
    "profile_bg":    "",
}

def get_img(key: str):
    url = IMAGES.get(key, "")
    return url if url else None

from discord.ext import commands

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Images(bot))
