from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_reply_main():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Получить справку-вызов на следующую сессию')
    keyboard_builder.button(text='Получить расписание занятий на сессию')
    keyboard_builder.adjust(1, 1)
    return keyboard_builder.as_markup(resizekeyboard=False, one_time_keyboard=True, input_field_placeholder='Выберите услугу: ')


def get_reply_identification():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text='Пройти идентификацию')
    keyboard_builder.button(text='Об идентификации')
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(resizekeyboard=False, one_time_keyboard=True, input_field_placeholder='Выберите действие: ')
