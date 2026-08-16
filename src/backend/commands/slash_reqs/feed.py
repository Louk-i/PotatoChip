import discord
from discord import app_commands
from discord.ext import commands
import random
from data.emotions.manager import emotion_engine
from responses.slash_reqs import feed as resp
from embeds.status import manager as status_manager
from config.commands.slash_reqs.feed import FEED_DELTA_MIN, FEED_DELTA_MAX

class FeedCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = resp.COMMAND_NAME, description = resp.COMMAND_DESC)
    @app_commands.describe(food = resp.FOOD_DES)
    async def feed(self, interaction: discord.Interaction, food: str):
        deltas = {}
        
        for emo in list(emotion_engine.gauges.keys()):
            delta = random.randint(FEED_DELTA_MIN, FEED_DELTA_MAX)
            deltas[emo] = delta
            emotion_engine.adjust_gauge(emo, delta)
            
        highest_emo = max(deltas, key=deltas.get)
        if deltas[highest_emo] <= 0:
            highest_emo = "none"
        
        category, _, _ = emotion_engine.get_dominant_emotion()
        await status_manager.update_eating_status(self.bot, food)
        
        message = resp.get_feed_response(food, highest_emo, category)
        await interaction.response.send_message(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(FeedCommand(bot))