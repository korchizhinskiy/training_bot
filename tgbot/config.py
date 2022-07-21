import configparser
from dataclasses import dataclass



@dataclass
class DatabaseConfig:
    user: str
    password: str
    host: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot
    database: DatabaseConfig


def load_config(path: str) -> Config:
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]
    database = config["database"]

    return Config(
            tg_bot=TgBot(
                token=tg_bot.get("token"),
                admin_id=tg_bot.getint("admin_id"),
                use_redis=tg_bot.getboolean("use_redis"),
            ),
            database=DatabaseConfig(**database)
    )
