import os
import json
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Настройки из переменных окружения (Render их подставит сам)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "shindaqwe")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Загрузка данных
with open("heroes.json", "r", encoding="utf-8") as f:
    HEROES = json.load(f)
with open("items.json", "r", encoding="utf-8") as f:
    ITEMS = json.load(f)
with open("letters.json", "r", encoding="utf-8") as f:
    LETTERS = json.load(f)

def get_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Случайный герой", callback_data="hero")],
        [InlineKeyboardButton(text="🎒 Случайный предмет", callback_data="item")],
        [InlineKeyboardButton(text="🔤 Случайная буква", callback_data="letter")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if CHANNEL_USERNAME:
        try:
            member = await bot.get_chat_member(f"@{CHANNEL_USERNAME}", message.from_user.id)
            if member.status in ("left", "kicked"):
                kb = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="✅ Подписаться", url=f"https://t.me/{CHANNEL_USERNAME}")
                ]])
                await message.answer("🔒 Подпишись на канал:", reply_markup=kb)
                return
        except Exception:
            pass
    await message.answer("🎮 **Dota Random**\n\nВыбери:", reply_markup=get_keyboard(), parse_mode="Markdown")

@dp.callback_query(lambda c: c.data in ["hero", "item", "letter"])
async def handle_random(callback: types.CallbackQuery):
    choice_type = callback.data
    if choice_type == "hero":
        result = random.choice(HEROES)
        text = f"🎲 Герой: **{result}**"
    elif choice_type == "item":
        result = random.choice(ITEMS)
        text = f"🎒 Предмет: **{result}**"
    else:
        result = random.choice(LETTERS)
        text = f"🔤 Буква: **{result}**"
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.message.answer("🔄 Ещё?", reply_markup=get_keyboard())
    await callback.answer()

async def main():
    print("✅ Бот запущен на Render!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())