import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

# Твои данные для запуска
TELEGRAM_TOKEN = "8571468939:AAGPUiMi8IjEp9F4qT0BxWGHbMDO_6rUNUo"
GEMINI_API_KEY = "AIzaSyCgWuxijS6eKvxlROp_JaYKkE7xZCmRgks"

# Настройка логирования (чтобы видеть ошибки в консоли Bothost)
logging.basicConfig(level=logging.INFO)

# Настройка нейросети Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Приветственное сообщение при нажатии /start
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я твой личный ИИ-помощник Gemini. Напиши мне любой вопрос!")

# Обработка входящих текстовых сообщений
@dp.message_handler()
async def chat_handler(message: types.Message):
    try:
        # Отправляем текст пользователя в нейросеть
        response = model.generate_content(message.text)
        
        # Проверяем, есть ли ответ
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Я не смог сгенерировать ответ, попробуй еще раз.")
            
    except Exception as e:
        logging.error(f"Ошибка бота: {e}")
        await message.answer("Произошла ошибка. Скорее всего, нужно проверить API ключ нейросети.")

if __name__ == '__main__':
    # Запуск бота в режиме бесконечного цикла
    executor.start_polling(dp, skip_updates=True)
