import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

# ТВОИ ДАННЫЕ
TOKEN = "8571468939:AAGPUiMi8IjEp9F4qT0BxWGHbMDO_6rUNUo"
API_KEY = "AIzaSyBhNWGjlvO_7cNjHwSBza7XIaMlicASKsA"

logging.basicConfig(level=logging.INFO)

# Инициализация
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Бот обновлен! Напиши что-нибудь.")

@dp.message_handler()
async def chat(message: types.Message):
    try:
        # Пытаемся получить ответ самым простым способом
        response = model.generate_content(message.text)
        
        # Выводим ответ
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Пустой ответ от ИИ.")
            
    except Exception as e:
        # Бот напишет точный текст ошибки прямо тебе в чат!
        error_message = f"❌ Ошибка: {str(e)}"
        logging.error(error_message)
        await message.answer(error_message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
