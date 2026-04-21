from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)
import random

from config.states import GAME
from handlers.start_handler import start

async def game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.user_data - словарь, который уникален для каждого человека
    # context.chat_data - словарь, который уникален для каждого чат
    # context.bot_data - словарь, который общий для всех
    keyboard = [["загадал"]]
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вы попали в игру! Загадайте число от 0 до 100. А бот попытается его угадать. Нажмите на кнопку",
        reply_markup=markup,
    )
    context.user_data["start"] = 0
    return GAME


async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # userdata = 0
    choise = update.effective_message.text
    print(context.user_data["start"])
    if choise == "загадал":
        keyboard = [[">", "<"], ["Угадал!"]]
        a = random.randint(1, 100)
        markup = ReplyKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{a}?", reply_markup=markup
        )
        context.user_data["start"] = 0
        context.user_data["end"] = 100
        context.user_data["a"] = a
    if choise == ">":
        context.user_data["start"] = context.user_data["a"]
        a = random.randint(context.user_data["start"], context.user_data["end"])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{a}?")
        context.user_data["a"] = a
    elif choise == "<":
        context.user_data["end"] = context.user_data["a"]
        a = random.randint(context.user_data["start"], context.user_data["end"])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{a}?")
        context.user_data["a"] = a
    elif choise == "Угадал!":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Угадал!")
        context.user_data["amount_games"] += 1
        context.user_data.pop("start")
        context.user_data.pop("end")
        context.user_data.pop("a")
        return await start(update, context)
    