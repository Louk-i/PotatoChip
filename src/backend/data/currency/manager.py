import os
import aiomysql
from config import settings
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv(os.path.join(os.path.dirname(__file__), '../../../../.env'))

DB_PASSWORD = os.getenv("DB_PASSWORD")
if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is not setup in the .env file")

class PotatoChipCurrencyManager:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        """inits the async connection pool, await when the bot starts"""
        self.pool = await aiomysql.create_pool(
            host = settings.DB_HOST,
            user = settings.DB_USER,
            password = settings.DB_PASSWORD,
            db = settings.DB_NAME,
            autocommit = settings.AUTOCOMMIT,
            minsize = settings.MIN_SIZE,
            maxsize = settings.MAX_SIZE 
        )
        await self._init_db()

    def _get_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    async def _init_db(self):
        """init the table on the db"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS economy (
                        user_id BIGINT PRIMARY KEY,
                        chips INT DEFAULT 0,
                        last_daily TIMESTAMP NULL DEFAULT NULL,
                        last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        claim_streak INT DEFAULT 0
                    )
                """)

    async def register_user(self, user_id: int):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    INSERT IGNORE INTO economy (user_id, last_modified)
                    VALUES (%s, %s)
                """, (user_id, self._get_now()))

    async def modify_chips(self, user_id: int, amount: int) -> int:
        """adds or removes chips. inits a user if they don't exist already in the db"""
        now = self._get_now()
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("""
                    INSERT INTO economy (user_id,  chips, last_modified)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        chips = chips + VALUES(chips),
                        last_modified = VALUES(last_modified)
                """, (user_id, amount, now))
                
                await cursor.execute("SELECT chips FROM economy WHERE user_id = %s", (user_id,))
                result = await cursor.fetchone()
                return result[0]

    async def can_claim_daily(self, user_id: int) -> tuple[bool, timedelta | None]:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT last_daily FROM economy WHERE user_id = %s", (user_id,))
                row = await cursor.fetchone()

        if not row or not row[0]:
            return True, None

        last_daily = datetime.fromisoformat(row[0])
        now = datetime.now(timezone.utc)
        time_since_last = now - last_daily
        cooldown = timedelta(hours=settings.DAILY_COOLDOWN_HOURS)

        if time_since_last >= cooldown:
            return True, None
        return False, cooldown - time_since_last

    async def update_daily(self, user_id: int) -> tuple[bool, int | timedelta, int | None]:
        """
        tries to claim the daily reward and also does a check
        returns a tuple: (success or not, new_balance OR time_remaining)
        """
        # cd chec k
        can_claim, time_left = await self.can_claim_daily(user_id)
        if not can_claim:
            return False, time_left, None

        now = datetime.now(timezone.utc)
        now_str = now.isoformat()
        
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # streak calc
                await cursor.execute("SELECT last_daily, claim_streak FROM economy WHERE user_id = %s", (user_id,))
                row = await cursor.fetchone()
                
                streak = 1 
                if row and row[0]:
                    last_daily = datetime.fromisoformat(row[0])
                    grace_period = timedelta(hours = settings.DAILY_GRACE_PERIOD_HOURS)
                    
                    # sanity check
                    if (now - last_daily) <= grace_period:
                        streak = (row[1] or 0) + 1
                
                reward = streak * settings.DAILY_REWARD_AMOUNT_MODIFIER
                
                # give reward, upd timestamp
                await cursor.execute("""
                    INSERT INTO economy (user_id, chips, last_daily, last_modified, claim_streak)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE 
                        chips = chips + VALUES(chips),
                        last_daily = VALUES(last_daily),
                        last_modified = VALUES(last_modified),
                        claim_streak = VALUES(claim_streak)
                """, (user_id, reward, now_str, now_str, streak))
                
                # return new chip counts
                await cursor.execute("SELECT chips FROM economy WHERE user_id = %s", (user_id,))
                result = await cursor.fetchone()
                
                return True, result[0], streak