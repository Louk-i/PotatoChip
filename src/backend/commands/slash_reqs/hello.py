import discord
from discord import app_commands
from discord.ext import commands
from data.emotions.manager import emotion_engine
from responses.slash_reqs import hello as resp

class HelloCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name =resp.COMMAND_NAME, description = resp.COMMAND_DESC)
    async def hello(self, interaction: discord.Interaction):
        # emotion fetch
        category, stage_name, stage_level = emotion_engine.get_dominant_emotion()
        
        # response string
        user_name = interaction.user.display_name
        message = resp.get_hello_response(category, stage_level, user_name)
        
        await interaction.response.send_message(message)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelloCommand(bot))