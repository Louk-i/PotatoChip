import discord
import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from router import router as bot_router
from embeds.status import manager as status_manager


load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        
        super().__init__(command_prefix = "p?", intents = intents)

    async def setup_hook(self):
        await bot_router.load_routes(self)
        print("log: initing commands")
        await self.tree.sync()
        print("log: commands synced successful")

bot = MyBot()

@bot.event
async def on_ready():
    await status_manager.update_mood_status(bot)
    print(f"logged in as {bot.user} (id: {bot.user.id})")

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("TokenNotFoundError")
    
    bot.run(token)