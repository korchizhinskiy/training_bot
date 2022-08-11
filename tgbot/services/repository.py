from asyncpg import Connection
import logging


class Repo():
    """Database abstraction class"""

    logger = logging.getLogger("Repo")
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )
    def __init__(self, connection: Connection):
        self.connection: Connection = connection

    
    async def add_user(self, user_id, user_first_name) -> bool:
        """Add user's info into database.'"""
        if not await self._is_user_in_database(user_id, user_first_name):
            await self.connection.execute(
                    """
                    INSERT INTO users (user_id, user_first_name)
                    VALUES ($1, $2);
                    """, *(user_id, user_first_name)
            )
            return True
        return False


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


class UserRepo():
    """User database class."""
    logger = logging.getLogger("UserRepo")
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            )

    def __init__(self, connection: Connection):
        self.connection = connection

    async def add_exercise_into_training_day(self, user_id, week_number, week_day, exercise_name, count_approaches, count_repetition) -> None:
        """Output all exercises from database."""
        await self.connection.execute(
                """
                INSERT INTO training (fk_user_id, fk_week_number, fk_week_day, exercise, count_approaches, count_repetition)
                VALUES ($1, $2, $3, $4, $5, $6)
                """, *(user_id, int(week_number), int(week_day), exercise_name, int(count_approaches), int(count_repetition))
                )

    async def add_training_day(self, user_id, week_number, week_day) -> None:
        """ Add training day into weeks table. """
        await self.connection.execute(
                """
                INSERT INTO weeks (fk_user_id, week_number, week_day)
                VALUES ($1, $2, $3);
                """, *(user_id, week_number, week_day)
                )


    async def delete_training_day(self, user_id, week_number, week_day) -> None:
        """ Add training day into weeks table. """
        await self.connection.execute(
                """
                DELETE FROM weeks
                WHERE fk_user_id = $1 AND week_number = $2 AND week_day = $3;
                """, *(user_id, week_number, week_day)
                )


    async def print_exercise(self) -> tuple[str]:
        """Output all exercises from database."""
        exercises = await self.connection.fetch(
                """
                SELECT exercise_name from exercises;
                """
                )
        result = tuple((exercise["exercise_name"] for exercise in exercises))
        return result


    async def print_chart_week_number(self, user_id) -> tuple[str]:
        """ Output user's training. """
        training = await self.connection.fetch(
                """
                SELECT (fk_week_number, fk_week_day, exercise, count_approaches, count_repetition) from users
                INNER JOIN training
                ON users.user_id = training.fk_user_id
                """
                )
        return training

    async def check_user_chart_week_number(self, user_id) -> tuple[int]:
        """ Check user's chart. """
        result = await self.connection.fetch(
                """
                SELECT DISTINCT (week_number) FROM weeks
                WHERE fk_user_id = $1
                """, user_id
                )
        weeks_list = tuple((weeks[0] for weeks in result )) 
        return weeks_list
    

    async def get_maximum_week_number(self, user_id) -> int:
        """ Get maximum week in table for user. """
        week = await self.connection.fetchval(
                """
                SELECT MAX(week_number) from weeks
                WHERE fk_user_id = $1;
                """, user_id
                )
        self.logger.debug(f"Результат - {week}")
        return week
    

    async def check_user_chart_week_day(self, user_id, week_number) -> tuple[int]:
        """ Check user's chart. """
        result = await self.connection.fetch(
                """
                SELECT DISTINCT (week_day) FROM weeks
                WHERE fk_user_id = $1 AND week_number = $2;
                """, *(user_id, week_number)
                )
        days_list = tuple((day[0] for day in result)) 
        self.logger.info(f"{days_list}")
        return days_list


    async def check_user_chart_exercises(self, user_id, week_number, week_day) -> tuple[int]:
        """ Check user's chart. """
        result = await self.connection.fetch(
                """
                SELECT (exercise, count_approaches, count_repetition, ordering) from training
                WHERE fk_user_id = $1 AND fk_week_number = $2 AND fk_week_day = $3
                ORDER BY ordering;
                """, *(user_id, week_number, week_day)
                )
#        exercise_list = tuple((exercise[0] for exercise in result )) 
        return result


class AdminRepo():
    """Administration database class."""
    logger = logging.getLogger("AdminRepo")
    logging.basicConfig(
            level=logging.DEBUG,
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


    async def change_exercise_info(self, exercise_name, new_exercise_name=None, new_exercise_description=None) -> None:
        """Change information about exercise in database."""
        if new_exercise_name:
            await self.connection.execute(
                    """
                    UPDATE exercises
                    SET exercise_name = $1
                    WHERE exercise_name = $2
                    """, *(new_exercise_name, exercise_name)
                    )
        else:
            await self.connection.execute(
                    """
                    UPDATE exercises
                    SET exercise_description = $1
                    WHERE exercise_name = $2
                    """, *(new_exercise_description, exercise_name)
                    )

        
    

    async def print_exercises(self) -> tuple[str]:
        """Output all exercises from database."""
        exercises = await self.connection.fetch(
                """
                SELECT exercise_name from exercises;
                """
                )
        result = tuple((exercise["exercise_name"] for exercise in exercises))
        return result


    async def check_exercise(self, exercise_name) -> bool:
        """ Check for the presence of an exercise. """
        result = await self.connection.fetch(
                """
                SELECT exercise_name FROM exercises
                WHERE exercise_name = $1;
                """, exercise_name
                )
        if result:
            return True
        else: 
            return False





