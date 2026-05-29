import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import ContextTypes

from config.states import GAME2,GAME2DIF
from handlers.start_handler import start
async def game_2_2start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("от 1 до 10", callback_data="easy")],
        [InlineKeyboardButton("от 1 до 100", callback_data="medium")],
        [InlineKeyboardButton("от 1 до 1000", callback_data="hard")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберете уровень сложности", reply_markup=markup)
    return GAME2DIF

async def game_2_2dif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # достаем уровень сложности из callback_data
    dif = query.data # easy/medium/hard

    if dif == 'easy':
        e = 10
    elif dif == 'medium':
        e = 100
    elif dif == 'hard':
        e = 1000
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f" Я загадал число от 1 до {e}!\n"
        "Попробуй угадать. Введи свой вариант:"
    )
    
    secret_number = random.randint(1, e)
    context.user_data['game_info'] = {
        'secret': secret_number,
        'attempts': 0,
        'min_range': 1,
        'max_range': e
    }
    
    return GAME2


async def game_2_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    guess = int(update.effective_message.text)

    secret = context.user_data["game_info"]['secret']


    if guess < secret:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f"📉 Загаданное число БОЛЬШЕ, чем {guess}\n")
    elif guess > secret:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f"📈 Загаданное число МЕНЬШЕ, чем {guess}\n")

    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,text=f" Поздравляю! Ты угадал число {secret}!\n"
        )
        return await start(update, context) 
        #del user_games[user_id]
