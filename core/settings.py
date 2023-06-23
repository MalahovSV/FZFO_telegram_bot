from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int

@dataclass
class DBConnectionOption:
    db_source: str
    user_sql: str
    password_sql: str
    host: str
    port: str


@dataclass
class Settings:
    bots: Bots
    str_connection: DBConnectionOption

def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=env.int("ADMIN_ID")
        ),
        str_connection=DBConnectionOption(
            db_source=env.str("DB_SOURCE"),
            user_sql=env.str("USER"),
            password_sql=env.str("PASSWORD"),
            host=env.str("HOST"),
            port=env.str("PORT")
        )
    )

settings = get_settings('input')