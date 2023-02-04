from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
from citilink import *
import time as tm
import utils as ut


bot = Bot(token='', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
CHANNEL_ID = ''
NOT_SUB_MESSAGE = 'Для доступа к функционалу, подпишитесь на канал'


# защита от спама
spams = {}
msgs = 4 # Messages in
max = 5 # Seconds
ban = 300 # Seconds
def is_spam(user_id):
    try:
        usr = spams[user_id]
        usr["messages"] += 1
    except:
        spams[user_id] = {"next_time": int(tm.time()) + max, "messages": 1, "banned": 0}
        usr = spams[user_id]
    if usr["banned"] >= int(tm.time()):
        return True
    else:
        if usr["next_time"] >= int(tm.time()):
            if usr["messages"] >= msgs:
                spams[user_id]["banned"] = tm.time() + ban
                # text = """You're banned for {} minutes""".format(ban/60)
                # bot.send_message(user_id, text)
                # User is banned! alert him...
                return True
        else:
            spams[user_id]["messages"] = 1
            spams[user_id]["next_time"] = int(tm.time()) + max
    return False
# конец защиты

def check_sub_channel(chat_member):  # Проверка на подписку
    print(chat_member['status'])

    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    if message.chat.type == 'private':
        if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button_1 = types.KeyboardButton(text="Начать")
            keyboard.add(button_1)
            await message.answer(
                'Рады вас видеть! Этот бот создан для быстрого поиска товара со скидкой из магазина Ситиилнк',
                reply_markup=keyboard)
        else:
            await message.answer(NOT_SUB_MESSAGE, reply_markup=ut.sub_menu)



@dp.message_handler(Text(equals='Начать'))
async def get_choice(message: types.Message):
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Процессоры", "Видеокарты", "Материнские платы"]
        keyboard.add(*buttons)
        await message.answer('Какие комплектующие вас интересуют?', reply_markup=keyboard)
    else:
        await message.answer(NOT_SUB_MESSAGE, reply_markup=ut.sub_menu)

@dp.callback_query_handler(text='subchanneldone')  # Что будет выводиться, если человек подписан
async def subchanneldone(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Процессоры", "Видеокарты", "Материнские платы"]
        keyboard.add(*buttons)
        await bot.send_message(message.from_user.id, 'Какие комплектующие вас интересуют?', reply_markup=keyboard)
    else:
        await message.answer(NOT_SUB_MESSAGE, reply_markup=ut.sub_menu)



def create_card(json_file):
    cards = []
    for index, i in enumerate(json_file):
        card = f'{hbold(i.get("name"))}\n' \
               f'{hbold(i.get("price") + " ₽")}\n' \
               f'{i.get("link")}'
        if index % 20 == 0:
            tm.sleep(5)
        cards.append(card)
    return cards


@dp.message_handler(Text(equals='Процессоры'))
async def result(message: types.Message):
    await message.answer('Ищем лучшее для вас')
    try:
        CPU()
        with open('CPU_citilink5%.json') as file:
            data = json.load(file)
            cards = create_card(data)
            for card in cards:
                await message.answer(card)
    except:
        await message.answer(
            'Сожалеем, но бот ничго не нашел, попробуйте позже, если ничего не получится, то обратитесь к администратору - https://t.me/KkkkkkkkKfh')


@dp.message_handler(Text(equals='Видеокарты'))
async def result(message: types.Message):
    await message.answer('Ищем лучшее для вас')
    try:
        video_cards()
        with open('Video_cards_citilink5%.json') as file:
            data = json.load(file)
            cards = create_card(data)
            for card in cards:
                await message.answer(card)
    except:
        await message.answer(
            'Сожалеем, но бот ничго не нашел, попробуйте позже, если ничего не получится, то обратитесь к администратору - https://t.me/KkkkkkkkKfh')


# конец видеокарты

@dp.message_handler(Text(equals='Материнские платы'))
async def result(message: types.Message):
    await message.answer('Ищем лучшее для вас')
    try:
        motherboard()

        with open('motherboard_citilink5%.json') as file:

            data = json.load(file)
            cards = create_card(data)
            for card in cards:
                await message.answer(card)
    except:
        await message.answer(
            'Сожалеем, но бот ничго не нашел, попробуйте позже, если ничего не получится, то обратитесь к администратору - https://t.me/KkkkkkkkKfh')


# Конец motherboard

@dp.message_handler(commands=['about_us'])
async def connection(message: types.Message):
    await message.answer('Вот кого ты ищешь - https://t.me/KkkkkkkkKfh')


@dp.message_handler()
async def info(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Упс, похоже что это неизвестная команда!\nСписок команд вы можете посмотреть в меню')


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
