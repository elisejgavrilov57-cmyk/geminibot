import os
import logging
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

# 1. Получаем ключи из настроек сервера (Environment Variables)
TELEGRAM_TOKEN = "8571468939:AAGPUiMi8IjEp9F4qT0BxWGHbMDO_6rUNUo"
GEMINI_API_KEY = "AIzaSyCgWuxijS6eKvxlROp_JaYKkE7xZCmRgks"

# 2. Настраиваем логирование, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

# 3. Инициализируем Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Инициализируем бота
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer("Бот успешно запущен через GitHub и Bothost! Напиши мне что-нибудь, и я отвечу.")

# Обработка любых текстовых сообщений
@dp.message_handler()
async def talk_to_ai(message: types.Message):
    try:
        # Отправляем запрос в нейросеть
        response = model.generate_content(message.text)
        
        # Если ответ от AI есть, отправляем его пользователю
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("AI не смог придумать ответ.")
            
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.answer("Произошла ошибка. Проверь настройки переменных TELEGRAM_TOKEN и GEMINI_API_KEY на хостинге.")

if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
