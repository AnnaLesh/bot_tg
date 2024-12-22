from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandObject
import keyboards as kb
import asyncio
import dotenv
import json
import os


dotenv.load_dotenv()
bot = Bot(token='8174847394:AAFr_E5o4gi24-g1LEIVQSGY62_hmNoHlks')
disp = Dispatcher()
users_points = {}


@disp.message(Command('start'))
async def start(message: types.Message):
    with open('user_points_counter_template.json', 'r', encoding='utf-8') as file:
        points_counter = json.load(file)
    users_points[message.from_user.id] = points_counter
    msg = 'Поздравляю, вы стали студентом КГУ! Вам предстоит изучить корпус Е, изучить все предметы и ответить на вопросы, собирая баллы - листочки курсовой. Сможете ли вы собрать их всех и сдать курсовую?'
    await message.answer(msg, reply_markup=kb.start_kb())


@disp.callback_query(F.data == 'choose_floor')
async def choose_floor(callback: types.CallbackQuery):
    not_finished_floors = []
    for floor in users_points[callback.from_user.id]:
        for section in users_points[callback.from_user.id][floor]:
            if users_points[callback.from_user.id][floor][section]['status'] == 'not_finished':
                not_finished_floors.append(floor)
                break
    if not_finished_floors == []:
        await end_quiz(callback)
    elif len(not_finished_floors) == 5:
        await callback.message.edit_reply_markup(reply_markup=kb.choose_floor_kb(not_finished_floors))
    else:
        await callback.message.edit_text('Куда пойдем дальше?', reply_markup=kb.choose_floor_kb(not_finished_floors))


@disp.callback_query(F.data.startswith('to_floor'))
async def go_to_floor(callback: types.CallbackQuery):
    chosen_floor = callback.data[8:]
    not_finished_sections = []
    sections = users_points[callback.from_user.id][chosen_floor]
    for section in sections:
        if users_points[callback.from_user.id][chosen_floor][section]['status'] == 'not_finished':
            not_finished_sections.append([section, list(sections.keys()).index(section)])
    if not_finished_sections == []:
        await choose_floor(callback)
    else:
        await callback.message.edit_text(f'{chosen_floor}. Куда пойдем?', reply_markup=kb.choose_section_kb(not_finished_sections, chosen_floor))


@disp.callback_query(F.data.startswith('to_section'))
async def go_to_section(callback: types.CallbackQuery):
    chosen_section_num = callback.data[10:callback.data.index('floor')]
    chosen_floor = callback.data[callback.data.index('floor') + 5:]
    chosen_section = list(users_points[callback.from_user.id][chosen_floor].keys())[int(chosen_section_num)]
    await next_question(callback, chosen_section, chosen_floor, 0)


async def next_question(callback: types.CallbackQuery,
                         chosen_section: str,
                         chosen_floor: str,
                         question_num: int):
    if question_num > 2:
        users_points[callback.from_user.id][chosen_floor][chosen_section]["status"] = 'finished'
        msg = f'Вы прошли эту секцию и набрали {users_points[callback.from_user.id][chosen_floor][chosen_section]["points"]} баллов'
        await callback.message.edit_text(msg, reply_markup=kb.end_section_keyboard(chosen_floor))
    else:
        with open('questions.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        question = data[chosen_floor][chosen_section][question_num]
        msg = question['question'] + '\n\nВарианты ответов:'
        for ans_variant in question['answer_variants']:
            msg += f'\n{question["answer_variants"].index(ans_variant) + 1}. {ans_variant}'
        image_path = question["image"]
        section_num = list(users_points[callback.from_user.id][chosen_floor].keys()).index(chosen_section)
        await callback.message.edit_text(msg, reply_markup=kb.question_kb(question_num, chosen_floor, section_num))
        await callback.message.answer_photo(photo=image_path)

@disp.callback_query(F.data.startswith('ans'))
async def read_answer(callback: types.CallbackQuery):
    with open('questions.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    ans_num = callback.data[3:4]
    question_num = int(callback.data[6:7])
    floor = f'{callback.data[9:10]} этаж'
    section_num = callback.data[callback.data.index('sn') + 2:]
    section = list(data[floor].keys())[int(section_num)]
    user_answer = data[floor][section][question_num]['answer_variants'][int(ans_num)]
    answer = data[floor][section][question_num]['answer']
    if user_answer == answer:
        users_points[callback.from_user.id][floor][section]['points'] += 1
    question_num += 1
    await next_question(callback, section, floor, question_num)


async def end_quiz(callback: types.CallbackQuery):
    total_points = 0
    for floor in users_points[callback.from_user.id]:
        for section in users_points[callback.from_user.id][floor]:
            total_points += users_points[callback.from_user.id][floor][section]['points']
    if total_points <= 17: msg = 'Ой, похоже вы не до конца разобрались с учебной программой…Но не расстраивайтесь, вы всегда можете попробовать еще раз!'
    elif total_points <= 23: msg = 'Поздравляю, вы справились с учебной программой и получили удовлетворительную оценку за курсовую работу!»'
    elif total_points <= 30: msg = 'Поздравляю, вы достойно справились с учебной программой и получили хорошую оценку за курсовую работу!'
    elif total_points <= 36: msg = 'Поздравляю, вы отлично справились с учебной программой и получили наивысшую оценку за курсовую работу!'
    await callback.message.edit_text(msg)


async def set_main_menu(bot: Bot):
    menu_commands = [
        types.BotCommand(command='/start',
                   description='Пройти заново')
    ]
    await bot.set_my_commands(menu_commands)


async def main():
    disp.startup.register(set_main_menu)
    await disp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
