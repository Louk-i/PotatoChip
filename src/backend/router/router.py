import logging
from config.settings import COMMAND_ROUTES

async def load_routes(bot):
    """dynamic loads all command modules into potato chip"""
    for route in COMMAND_ROUTES:
        try:
            await bot.load_extension(route)
            logging.info(f"successfully loaded route: {route}")
        except Exception as e:
            logging.error(f"failed to load route {route}: {e}")

async def load_routes(bot):
    """dynamic loads all command modules into potato chip"""
    for route in COMMAND_ROUTES:
        try:
            await bot.load_extension(route)
            logging.info(f"successfully loaded route: {route}")
        except Exception as e:
            logging.error(f"failed to load route {route}: {e}")