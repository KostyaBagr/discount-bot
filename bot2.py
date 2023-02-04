from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token='5983778797:AAGCjkJqN0wnVkCAzCeBT5JtZIxDgQC0N7s', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(text='start')  # Что будет выводиться, если человек подписан
async def start(message: types.Message):
    start_buttons = ["Процессоры", "Видеокарты", "Материнские платы"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Какие комплектующие вас интересуют?', reply_markup=keyboard)


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()