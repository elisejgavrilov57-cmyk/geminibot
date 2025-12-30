import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types

# ТВОИ ДАННЫЕ
TELEGRAM_TOKEN = "8571468939:AAGPUiMi8IjEp9F4qT0BxWGHbMDO_6rUNUo"
GEMINI_API_KEY = "AIzaSyBhNWGjlvO_7cNjHwSBza7XIaMlicASKsA"

# Логирование
logging.basicConfig(level=logging.INFO)

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Бот
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Я перезагружен и готов к работе! Спроси меня о чем-нибудь.")

@dp.message_handler()
async def chat_handler(message: types.Message):
    try:
        # Попытка получить ответ
        response = model.generate_content(message.text)
        
        # Проверяем, есть ли текст в ответе
        if hasattr(response, 'text') and response.text:
            await message.answer(response.text)
        else:
            # Бывает, что Gemini блокирует ответ из-за цензуры
            await message.answer("Хм, я не могу ответить на этот вопрос из-за настроек безопасности или пустой генерации.")
            
    except Exception as e:
        logging.error(f"Error: {e}")
        # Выводим саму ошибку, чтобы понять, в чем дело
        await message.answer(f"Ошибка API: {str(e)[:100]}...")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    
