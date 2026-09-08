import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import google.generativeai as genai

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Студент"), KeyboardButton(text="IT-технології")],
        [KeyboardButton(text="Контакти"), KeyboardButton(text="Prompt AI")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Вітаю! Оберіть опцію з меню:", reply_markup=menu_keyboard)

@dp.message(F.text == "Студент")
async def handle_student(message: types.Message):
    text = "Студент: Непотачев Іван Дмитрович\nГрупа: ІА-32\nВаріант: 12"
    await message.answer(text)

@dp.message(F.text == "IT-технології")
async def handle_tech(message: types.Message):
    text = (
        "Мій стек технологій (Full-Stack):\n"
        "- JavaScript / TypeScript\n"
        "- Node.js (Express, NestJS)\n"
        "- React, Redux Toolkit\n"
        "- PostgreSQL, MongoDB, Redis\n"
        "- Docker"
    )
    await message.answer(text)

@dp.message(F.text == "Контакти")
async def handle_contacts(message: types.Message):
    text = "Контакти:\nEmail: ivan.nepotachev@example.com\nTelegram: @your_username"
    await message.answer(text)

@dp.message(F.text == "Prompt AI")
async def handle_prompt_ai(message: types.Message):
    await message.answer("Напишіть ваше запитання до штучного інтелекту:")

@dp.message()
async def handle_ai_request(message: types.Message):
    try:
        await bot.send_chat_action(chat_id=message.chat.id, action="typing")
        response = await model.generate_content_async(message.text)
        await message.answer(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("Помилка при зверненні до AI. Спробуйте пізніше.")

async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())