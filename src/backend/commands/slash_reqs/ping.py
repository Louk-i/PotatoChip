import discord
from discord import app_commands
from discord.ext import commands
from responses.slash_reqs import ping as resp

class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = resp.COMMAND_NAME, description = resp.COMMAND_DESC)
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)

        await interaction.response.send_message(resp.get_ping_response(latency_ms))

async def setup(bot: commands.Bot):
    await bot.add_cog(PingCommand(bot))