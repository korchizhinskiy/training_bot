import asyncpg
from asyncpg import Connection
import logging


class Repo():
    """Database abstraction class"""

    logger = logging.getLogger(__name__)
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )
    def __init__(self, connection: Connection):
        self.connection: Connection = connection

    
    async def add_user(self, user_id, user_name) -> None:
        await self.check_user(user_id)
        for k in range(10000):
            await self.connection.execute(
                    f"""
                    INSERT INTO users (user_id, user_first_name)
                    VALUES ({user_id}, '{user_name}');
                    """)
            print(k)

    async def check_user(self, user_id) -> bool:
#        db_user = await self.connection.execute(
#                f"""
#                SELECT user_first_name FROM users
#                WHERE user_id = {user_id};
#                """
#                )
        user = await self.connection.fetch(
                f"""
                SELECT * FROM users
                """
                )
        self.logger.info(f"Пользователь найден")
        return True




