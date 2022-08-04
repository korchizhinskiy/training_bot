from typing import Generator
from asyncpg import Connection
import logging


class Repo():
    """Database abstraction class"""

    logger = logging.getLogger("Repo")
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )
    def __init__(self, connection: Connection):
        self.connection: Connection = connection

    
    async def add_user(self, user_id, user_first_name) -> None:
        """Add user's info into database.'"""
        if not await self._is_user_in_database(user_id, user_first_name):
            await self.connection.execute(
                    """
                    INSERT INTO users (user_id, user_first_name)
                    VALUES ($1, $2);
                    """, *(user_id, user_first_name)
            )


    async def _is_user_in_database(self, user_id, user_first_name) -> bool:
        """Check information about user in database."""
        user = await self.connection.fetch(
                """
                SELECT user_id, user_first_name FROM users
                WHERE user_id = $1
                """, *(user_id,)
        )
                
        if user:
            # Change first_name in database, if them was changed since last using bot.
            if user[0]['user_first_name'] != user_first_name:
                await self._update_user_info(user_id, user_first_name)

            self.logger.info(f"\nПользователь: \n"
                             f"С ID: {user[0]['user_id']}\n"
                             f"С именем: {user[0]['user_first_name']} найден.\n")
            return True

        else:
            self.logger.info(f"\nПользователь: \n"
                             f"С ID: {user_id}\n"
                             f"С именем: {user_first_name} занесен в базу данных.\n")
            return False


    async def _update_user_info(self, user_id, user_first_name) -> None:
        """Update user's information in database.'"""
        await self.connection.execute(
                    """
                    UPDATE users 
                    SET user_first_name = $1
                    WHERE user_id = $2
                    """, *(user_first_name, user_id)
                )



class AdminRepo():
    """Administration database class."""
    logger = logging.getLogger("AdminRepo")
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )

    def __init__(self, connection: Connection):
        self.connection = connection


    async def add_exercise(self, exercise_name, exercise_description) -> None:
        """Add exercise's information into database."""
        await self.connection.execute(
                """
                INSERT INTO exercises (exercise_name, exercise_description)
                VALUES ($1, $2);
                """, *(exercise_name, exercise_description)
                )        
    

    async def delete_exercise(self, exercise_name) -> str:
        """Delete exercise's information from database."""
        return await self.connection.execute(
                """
                DELETE FROM exercises
                WHERE exercise_name = $1;
                """, exercise_name
                )


    async def change_exercise_info(self) -> None:
        """Change information about exercise in database."""
        pass
    

    async def print_exercises(self) -> tuple[str]:
        """Output all exercises from database."""
        exercises = await self.connection.fetch(
                """
                SELECT exercise_name from exercises;
                """
                )
        result = tuple((exercise["exercise_name"] for exercise in exercises))
        self.logger.info(result)
        
        return result





