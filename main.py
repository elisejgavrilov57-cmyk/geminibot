import os
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

# Получаем ключи из переменных окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")

logging.basicConfig(level=logging.INFO)

# Правильная настройка модели
genai.configure(api_key=API_KEY)
# Используем просто "gemini-1.5-flash" без лишних префиксов
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Система обновлена! Напиши мне что-нибудь.")

@dp.message_handler()
async def chat(message: types.Message):
    try:
        response = model.generate_content(message.text)
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("ИИ вернул пустой ответ.")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
