from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from core.db.dbconnect import Request
from core.utils.statesform import StepsIdentification


async def get_telegram_id(message: Message, state: FSMContext):
    await message.answer(f'{message.from_user.first_name}, введите логин: ')
    await state.set_state(StepsIdentification.GET_LOGIN)


async def get_login(message: Message, state: FSMContext):
    await  message.answer(f'Введён логин: \r\n{message.text}\r\nВведите пароль:')
    await state.update_data(login=message.text)
    await state.set_state(StepsIdentification.GET_PASSWORD)

async def get_password(message: Message, state: FSMContext, request: Request):
    await state.update_data(password=message.text)
    context_data = await state.get_data()
    result = await request.add_id_telegram(context_data.get('login'), context_data.get('password'), message.from_user.id)
    print(result)
    await message.delete()
    if result:
        await message.answer('ID учетной записи телеграм внесён в БД.\r\nВведите команду: start.',
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Ваши логин и/или пароль не верны.\n\rВы можете пройти идентификацию ещё раз.')
    await state.clear()

