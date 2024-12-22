from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def start_kb():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(InlineKeyboardButton(text='Зайти в корпус', callback_data='choose_floor'))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def choose_floor_kb(floors: list):
    keyboard_builder = InlineKeyboardBuilder()
    for floor in floors:
        keyboard_builder.add(InlineKeyboardButton(text=floor, callback_data=f'to_floor{floor}'))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def choose_section_kb(sections: list, floor):
    keyboard_builder = InlineKeyboardBuilder()
    for section in sections:
        keyboard_builder.add(InlineKeyboardButton(text=section[0], callback_data=f'to_section{section[1]}floor{floor}'))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def question_kb(question_num, floor_num, section_num):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(InlineKeyboardButton(text='1.', callback_data=f'ans0qn{question_num}fn{floor_num}sn{section_num}'))
    keyboard_builder.add(InlineKeyboardButton(text='2.', callback_data=f'ans1qn{question_num}fn{floor_num}sn{section_num}'))
    keyboard_builder.add(InlineKeyboardButton(text='3.', callback_data=f'ans2qn{question_num}fn{floor_num}sn{section_num}'))
    keyboard_builder.add(InlineKeyboardButton(text='4.', callback_data=f'ans3qn{question_num}fn{floor_num}sn{section_num}'))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


def end_section_keyboard(floor):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.add(InlineKeyboardButton(text='Продолжить', callback_data=f'to_floor{floor}'))
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()