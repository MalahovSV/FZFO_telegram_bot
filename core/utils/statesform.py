from aiogram.fsm.state import StatesGroup, State


class StepsIdentification(StatesGroup):
    GET_LOGIN = State()
    GET_PASSWORD = State()