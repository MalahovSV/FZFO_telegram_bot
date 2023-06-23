import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from core.handlers.basic import get_start, get_doc_help_call, get_help, get_contacts
from core.settings import settings
from core.utils.commands import set_commands
from core.middleware.dbmiddleware import DbSession
import asyncpg
from core.handlers import identification
from core.utils.statesform import StepsIdentification

async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')


async def create_pool():
    return await asyncpg.create_pool(user=settings.str_connection.user_sql,
                                             password=settings.str_connection.password_sql,
                                             host=settings.str_connection.host,
                                             port=settings.str_connection.port,
                                             database=settings.str_connection.db_source)


async def start():
    bot = Bot(token=settings.bots.bot_token)
    logging.basicConfig(level=logging.INFO)
    pool_connect = await create_pool()
    dp = Dispatcher()
    dp.update.middleware.register(DbSession(pool_connect))

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(identification.get_login, StepsIdentification.GET_LOGIN)
    dp.message.register(identification.get_password, StepsIdentification.GET_PASSWORD)
    dp.message.register(identification.get_telegram_id, Text(text="Пройти идентификацию"))
    dp.message.register(get_doc_help_call, Text(text="Получить справку-вызов на следующую сессию"))


    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.message.register(get_contacts, Command(commands=['contacts']))
    dp.message.register(get_help, Command(commands=['help']))
    dp.message.register(identification.get_telegram_id, Command(commands="identification"))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
