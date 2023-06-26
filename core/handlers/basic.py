from aiogram import Bot
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hlink

from core.keyboards.reply import get_reply_identification, get_reply_main
from core.db.dbconnect import Request
from core.utils.PrintDocument import create_help_call

async def get_start(message: Message, bot: Bot, request: Request):
    result = await request.check_telegram_id(message.from_user.id)
    if result:
        await message.answer(f'Здравствуйте {message.from_user.full_name}!',reply_markup=get_reply_main())
    else:
        await message.answer('Пользователь не опознан', reply_markup=get_reply_identification())

async def get_doc_help_call(message: Message, request: Request):

    doc_help_call = FSInputFile(await create_help_call(message.from_user.id, request))
    await message.reply_document(doc_help_call, caption='Ваша справка-вызов на следующую сессию:')

async def get_help(message: Message):
    await message.reply(f'Данный бот был разработан для кафедры заочной формы обучения Рубцовского индустриального института.\n\r'
                        f'\n\rБот оказывает услуги по предоставлению справки-вызова на сессию, а так же служит оповещательным каналом.\n\r'
                        f'\n\rЧтобы начать работу с ботом, необходимо ввести команду /start, после чего будет произведена Ваша идентификация.\n\r'
                        f'\n\rДля прохождения идентификации необходимы логин и пароль, которые Вы можете получить очно на кафедре ФЗФО (кабинет 344).\n\r'
                        f'\n\rЕсли Ваши логин и пароль верны, то бот запомнит данный телеграм-профиль, и далее Вы будете получать безпрепятственный доступ к сервисам данного бота.')


async def get_help_identification(message: Message):
    await message.reply(
        f'Чтобы пройти идентификацию, Вам необходимо ввести поочередно (согласно инструкциям приходящим от бота) ввести логин и пароль.\n\r'
        f'\n\rВ случае успешной идентификации в БД будет записан Ваш ID({message.from_user.id}) телеграм профиля.'
        f'Далее необходимо снова выполнить команду /start, после чего бот распознает Вас как студента ФЗФО и предоставит все свои услуги.\n\r'
        f'Если Ваши логин и пароль не вопринимаются ботом как верные, то Вам необходимо будет подойти к кабинету 344 (кафедра ФЗФО) или же обратиться к техническим специалистам (кабинет 221)'
    )


async def get_contacts(message: Message):
    await message.reply(
        f'Декан ФЗФО: Маршалов Эдуард Сергеевич\n\r'
        f'Номер городского телефона: 2-93-26\n\r'
        f'Электронная почта: fzfo2013@yandex.ru\n\r'
        f'Аудитория №344\n\r'
    )

async def get_plan_lessons(message: Message):
    await message.reply_sticker(r'CAACAgIAAxkBAAJY4mSCAROHKmnsm2rPnwxn8KzDfwiKAAIhDQACVCAISjI6cvLpMDtzLwQ')