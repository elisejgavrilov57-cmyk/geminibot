import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

# ТВОИ ОБНОВЛЕННЫЕ ДАННЫЕ
TELEGRAM_TOKEN = "8571468939:AAGPUiMi8IjEp9F4qT0BxWGHbMDO_6rUNUo"
GEMINI_API_KEY = "AIzaSyBhNWGjlvO_7cNjHwSBza7XIaMlicASKsA"

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Настройка бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Бот запущен с новым ключом Gemini! Теперь я готов общаться.")

@dp.message_handler()
async def chat_handler(message: types.Message):
    try:
        # Запрос к нейросети
        response = model.generate_content(message.text)
        
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Я получил пустой ответ от системы.")
            
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Произошла ошибка. Проверь консоль на хостинге.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
