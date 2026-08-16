import discord
from discord.ext import commands
import asyncio
from data.emotions.manager import emotion_engine
from config.embeds.status.status import EATING_STATUS_DURATION

STATUS_MAP = {
    "happy": discord.Status.online,
    "loud": discord.Status.online,
    "sad": discord.Status.idle,
    "quiet": discord.Status.idle,
    "angry": discord.Status.dnd,
    "fear": discord.Status.dnd,
}

_eating_timer_task: asyncio.Task | None = None

def get_current_discord_status() -> discord.Status:
    category, _, _ = emotion_engine.get_dominant_emotion()
    return STATUS_MAP.get(category, discord.Status.online)

async def update_mood_status(bot: commands.Bot):
    status = get_current_discord_status()
    await bot.change_presence(status = status, activity = None)

async def update_eating_status(bot: commands.Bot, food: str):
    global _eating_timer_task

    if _eating_timer_task and not _eating_timer_task.done():
        _eating_timer_task.cancel()

    activity = discord.CustomActivity(name = f"Eating: {food}")
    status = get_current_discord_status()

    await bot.change_presence(status=status, activity=activity)

    _eating_timer_task = asyncio.create_task(
        _clear_eating_status_after_delay(bot, EATING_STATUS_DURATION)
    )

async def _clear_eating_status_after_delay(bot: commands.Bot, delay_seconds: int):
    try:
        await asyncio.sleep(delay_seconds)
        await update_mood_status(bot)
    except asyncio.CancelledError:
        pass