import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
import aioredis
import pandasss
from aiogram.contrib.fsm_storage.memory import MemoryStorage




API_TOKEN = '6024972811:AAHcXpcJHMGJn9B0t1pCE_LKqiQWPMLWD7k'  # Замените на свой токен

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Создаем состояние для ожидания кода
class WaitForCode(StatesGroup):
    waiting_for_code = State()

# Создаем словарь для хранения кодов пользователей
saved_code = {}

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    await WaitForCode.waiting_for_code.set()
    await message.reply("Пожалуйста, отправьте ваш код.")


# Обработчик текстового сообщения после команды /start
@dp.message_handler( state=WaitForCode.waiting_for_code)
async def save_code(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print("Обработчик waiting for code активирован")
    text = message.text


    if text in pandasss.codes:

        saved_code[user_id] = text
        answer, owner = pandasss.bonus_amount(text)
        await state.finish()
    else:
        answer = 'Код не найден, попробуйте ввести код еще раз'
    # current_state = await state.get_state()
    # await message.answer(f"Текущее состояние: {current_state}")
   
    # Сбрасываем состояние
    
    print('обработчик waiting for code завершен')

    await message.reply(f'Владелец карты - {owner} \nНа счету {answer} баллов')



# Команда для отображения сохраненного кода
@dp.message_handler(commands=['showcode'])
async def show_code(message: types.Message):
    user_id = message.from_user.id
    if user_id in saved_code:
        code = saved_code[user_id]
        await message.reply(f"Ваш сохраненный код:\n```\n{code}\n```", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("У вас нет сохраненного кода.")
    await dp.storage.close()

@dp.message_handler(commands=["*"])  # Обработчик для любого состояния
async def check_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.answer(f"Текущее состояние: {current_state}")



if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)




