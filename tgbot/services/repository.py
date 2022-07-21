class Repo():
    """Database abstraction class"""

    def __init__(self, connection):
        self.connection = connection

    
    async def add_user(self, user_id, user_name) -> None:
        await self.connection.execute(f"""
                INSERT INTO users (user_id, user_first_name)
                VALUES ({user_id}, '{user_name}');
                """)

