import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "potato_chip")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is not set up in the .env file (settings.py)")

# commands
COMMAND_ROUTES = [
    "commands.slash_reqs.ping",
    "commands.slash_reqs.hello",
    "commands.slash_reqs.feed",
]

# currency
DAILY_REWARD_AMOUNT_MODIFIER = 10
DAILY_COOLDOWN_HOURS = 24
DAILY_GRACE_PERIOD_HOURS = 48
# currency db
MIN_SIZE = 1
MAX_SIZE = 10