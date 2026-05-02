import os
import json
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

# Настройки
BOT_TOKEN = "8705011374:AAE153SIL2UURVUKGB8zkma-G4P7N7-RKJo"  # Вставь свой токен

# Каналы для подписки
CHANNELS = [
    "shindaqwe",
    # "channel_2",
]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Загрузка данных
with open("heroes.json", "r", encoding="utf-8") as f:
    HEROES = json.load(f)
with open("items.json", "r", encoding="utf-8") as f:
    ITEMS = json.load(f)
with open("letters.json", "r", encoding="utf-8") as f:
    LETTERS = json.load(f)

def get_gate_keyboard():
    kb = []
    for i in range(0, len(CHANNELS), 2):
        row = []
        for j in range(2):
            idx = i + j
            if idx < len(CHANNELS):
                ch = CHANNELS[idx]
                row.append(InlineKeyboardButton(
                    text=f"Подписаться #{idx + 1}",
                    url=f"https://t.me/{ch}"
                ))
        kb.append(row)
    kb.append([InlineKeyboardButton(text="Проверить ✅", callback_data="check_subs")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Случайный герой", callback_data="hero")],
        [InlineKeyboardButton(text="🎒 Случайный предмет", callback_data="item")],
        [InlineKeyboardButton(text="🔤 Случайная буква", callback_data="letter")]
    ])

async def is_subscribed_to_all(user_id: int) -> bool:
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(f"@{ch}", user_id)
            if member.status in ("left", "kicked"):
                return False
        except Exception:
            return False
    return True

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if await is_subscribed_to_all(message.from_user.id):
        await message.answer(
            "🎮 **Dota Random Generator**\n\nВыбери:",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            "⚠️ Подпишись на каналы и нажми **'Проверить'**",
            reply_markup=get_gate_keyboard()
        )

@dp.callback_query(lambda c: c.data == "check_subs")
async def handle_check(callback: types.CallbackQuery):
    if await is_subscribed_to_all(callback.from_user.id):
        await callback.message.edit_text("✅ Доступ открыт!")
        await callback.message.answer(
            "🎮 **Dota Random Generator**",
            reply_markup=get_main_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.answer("❌ Не все каналы подписаны!", show_alert=True)

@dp.callback_query(lambda c: c.data in ["hero", "item", "letter"])
async def handle_random(callback: types.CallbackQuery):
    choice = callback.data
    if choice == "hero":
        txt = f"🎲 Герой: **{random.choice(HEROES)}**"
    elif choice == "item":
        txt = f"🎒 Предмет: **{random.choice(ITEMS)}**"
    else:
        txt = f"🔤 Буква: **{random.choice(LETTERS)}**"
    await callback.message.answer(txt, parse_mode="Markdown")
    await callback.message.answer("🔄 Ещё?", reply_markup=get_main_keyboard())
    await callback.answer()

async def on_startup(dp):
    print("✅ Бот запущен на Render!")
    print(f"📢 Каналов: {len(CHANNELS)}")

async def on_shutdown(dp):
    print("⏹️ Бот остановлен")
    await bot.close()

if __name__ == "__main__":
    from aiogram.executor import Executor
    executor = Executor(dp, skip_updates=True)
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
    executor.start_polling()