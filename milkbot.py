import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
import aioredis
import pandasss
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os



API_TOKEN = '6024972811:AAHcXpcJHMGJn9B0t1pCE_LKqiQWPMLWD7k'  # Замените на свой токен

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

# Создаем состояние для ожидания кода
class WaitForCode(StatesGroup):
    waiting_for_code = State()

class Back(StatesGroup):
    go_back = State()

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_button = KeyboardButton("Старт")
start_keyboard.add(start_button)
# Создаем словарь для хранения кодов пользователей
saved_code = {}

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id

    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False)

    button1 = KeyboardButton('⭐ Узнать количество бонусов')
    keyboard.add(button1)
    button2 = KeyboardButton('📒 Каталог продукции')
    keyboard.add(button2)
    button3 = KeyboardButton('📍Адреса фирменных киосков')
    keyboard.add(button3)
    button4 = KeyboardButton('☎️Служба поддержки')
    keyboard.add(button4)
    button5 = KeyboardButton('🪩 Мы в Instagram')
    keyboard.add(button5)
    button6 = KeyboardButton('📃 Условия покупательского клуба ML')
    keyboard.add(button6)
    button7 = KeyboardButton('💵 Цены на товары')
    keyboard.add(button7)
    
    
    await message.reply("Сәлеметсіз бе! Мен көмекші бот MilkyBot. Әрекетті таңдаңыз.", reply_markup=keyboard)
    await message.reply("Здравствуйте! Я бот помощник MilkyBot. Выберите действие")

    

# ------------------------------------------------------------

@dp.message_handler(Text(equals='⭐ Узнать количество бонусов'))
async def hooray(message: types.Message):

    await WaitForCode.waiting_for_code.set()
    # await Back.go_back.set()

    keyboard = ReplyKeyboardMarkup(resize_keyboard=False)
    button1 = KeyboardButton('Назад')
    keyboard.add(button1)

    await message.answer('Cәлеметсіз бе! Сіздің шотыңыздағы жинақталған бонустарды тексеру үшін бонустық картаның штрих-кодын жіберіңіз.', reply_markup=keyboard)

    await message.answer('Здравствуйте! Отправьте штрих-код бонусной карты для проверки накопленных бонусов на вашем счету.')
   

# --------------------------------------



#Для отправки файла условия бонусной карты   
async def send_file(chat_id):
    # Замените 'file_path' на путь к вашему файлу
    # file_path = 'C:/Users/User/Desktop/milky bot tg/uslov.docx'
    file_path1 = 'C:/Users/User/Desktop/milky bot tg/uslov_rus.docx'
    file_path2 = 'C:/Users/User/Desktop/milky bot tg/uslov_kaz.docx'
    
    # Отправляем файл
    with open(file_path1, 'rb') as file1:
        await bot.send_document(chat_id, file1)

    
    with open(file_path2, 'rb') as file2:
        await bot.send_document(chat_id, file2)


# --------------------------------------

# Отправьте фотографии
@dp.message_handler(Text(equals='💵 Цены на товары'))
async def hooray(message: types.Message):
    await send_pdf(message.chat.id)


async def send_pdf(chat_id):
    path = os.path.abspath('C:/Users/User/Desktop/milky bot tg/Прайс-лист фирменных киосков “MilkyLand”.pdf')
    with open(path, 'rb') as pdf_prices:

        await bot.send_document(chat_id, pdf_prices, caption='Цены на товары')



#---------------------------------------
@dp.message_handler(Text(equals='📃 Условия покупательского клуба ML'))
async def hooray(message: types.Message):
    await message.answer('Сатып алушы клубының ережелері мен шарттарын мына жерден көруге болады: http://milkyland.kz/club')
    await message.answer('Условия покупательского клуба вы можете просмотреть тут: http://milkyland.kz/club')
    await send_file(message.chat.id)

# --------------------------------------



@dp.message_handler(Text(equals='📒 Каталог продукции'))
async def hooray(message: types.Message):
    await message.answer('Каталогты көру үшін сілтемені басыңыз: http://milkyland.kz/product_line')

    await message.answer('Каталог доступен по ссылке: http://milkyland.kz/product_line')



# --------------------------------------



@dp.message_handler(Text(equals='📍Адреса фирменных киосков'))
async def hooray(message: types.Message):
    await message.answer('https://2gis.kz/aktobe/geo/70000001036503049')
    await message.answer('''
11 мкр., за ТД «Нектар», мини-рынок «Табыс»\n
8 мкр., за мини - рынком, напротив маг. «Анвар»\n
12 мкр., мини - рынок «Табыс»\n
ул. 101 Стр. бр., мини - рынок «Табыс»\n
ост. «Дом ветеранов», около «Дастархан»\n
р-и Жилгородок, мини-рынок «Табыс»\n
ж/м «Нур - Актобе, Каргалы, 15 (ТД «Сити»)\n
ул. Актанова, 59, напротив «Арай»\n
ул. Есет батыра, 105 около ТД «Жанар»\n
р-и «Малышка», ул. Заводская, 43\n
пр. Абилкайыр-хана, 6, ост. «Спутник»\n
ул. Сатпаева, 11, 23 школаул. Ш. Калдаякова, 276, около ТД "Сабыр"\n
ул. Шернияза, 54, напротив «Музыкального колледжа»\n
ул. Кереева, 2а, мини-рынок «Табыс»\n
р-н Гмз, ул. Гастелло, 185, мини-рынок «Табыс»\n
пр. А. Молдагуловой, 30а, рынок "Алия", молочный отдел\n
г. Хромтау, ул. Есет батыра, 3в, около ТД «Баян»\n
г. Хромтау, пр. Абая, 10 около ТД «даулетияр»''')



# --------------------------------------



# Для показа номера службы поддержки
@dp.message_handler(Text(equals='☎️Служба поддержки'))
async def hooray(message: types.Message):

    await message.answer('Қолдау қызметі нөмірі: +7-771-650-50-04')

    await message.answer('Номер службы поддержки: +7-771-650-50-04')


# --------------------------------------


@dp.message_handler(Text(equals='🪩 Мы в Instagram'))
async def hooray(message: types.Message):
    await message.answer('https://www.instagram.com/p/CpuF1hHM9s2/?igshid=MzRlODBiNWFlZA==')


# --------------------------------------


# На случай если пользователь случайно нажал на "Узнать бонусы". Этот обработчик заканчивает состояние ожидания штрих кода и возвращает клавиатуру меню
@dp.message_handler(Text(equals='Назад'), state="*")
async def goBack(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == WaitForCode.waiting_for_code.state:
        await state.finish()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=False)

    button1 = KeyboardButton('⭐ Узнать количество бонусов')
    keyboard.add(button1)
    button2 = KeyboardButton('📒 Каталог продукции')
    keyboard.add(button2)
    button3 = KeyboardButton('📍Адреса фирменных киосков')
    keyboard.add(button3)
    button4 = KeyboardButton('☎️Служба поддержки')
    keyboard.add(button4)
    button5 = KeyboardButton('🪩 Мы в Instagram')
    keyboard.add(button5)
    button6 = KeyboardButton('📃 Условия покупательского клуба ML')
    keyboard.add(button6)
    button7 = KeyboardButton('💵 Цены на товары')
    keyboard.add(button7)
    
    await message.reply("Әрекетті таңдаңыз")

    await message.reply("Выберите действие", reply_markup=keyboard)
    
# --------------------------------------

# Обработчик штрих кода после команды /Узнать количество бонусов
@dp.message_handler(state=WaitForCode.waiting_for_code)
async def save_code(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print("Обработчик waiting for code активирован")
    text = message.text

    owner = None

    if text in pandasss.codes:

        saved_code[user_id] = text
        answer, owner = pandasss.bonus_amount(text)
        await state.finish()
        await message.reply(f'Карта иесі - {owner} \nСiздiң шотыңызда {answer} балл')
        await message.reply(f'Владелец карты - {owner} \nНа счету {answer} баллов')

    else:
        # answer = 'Проверьте корректно ли введены данные'
        await message.reply(f'Деректердің дұрыс енгізілгенін тексеріңіз')
        await message.reply(f'Проверьте корректно ли введены данные')
       
    # Сбрасываем состояние
    
    print('обработчик waiting for code завершен')

    # await message.reply(f'Владелец карты - {owner} \nНа счету {answer} баллов')

# --------------------------------------

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




