import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
import random
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

MAINMENU, TALK, GAME = range(3)


# callback
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная инфа о том, что произошло
    # update.effective_user - полная инфа о человеке
    # update.effective_chat - полная инфа о чате
    #  update.effective_message - полная инфа о сообщении
    if 'amount_games' not in context.user_data:
        context.user_data['amount_games'] = 0 
    keyboard = [[InlineKeyboardButton('Режим разговора', callback_data='talk')]]

    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"привет,{update.effective_user.first_name}\n\nУ тебя {context.user_data["amount_games"]} игр(а)\n\nВ моем боте есть функции:\n"
        + "/talk - поговорить с gpt\n"
        + "/game-поиграть в игру"
        + "\nинформация о вас{update.effective_user}",
        reply_markup=markup,
    )

    return MAINMENU


async def biba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="боба")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.effective_user
    )


async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вы попали в режим разговора! Напишите что-то и бот вам ответит",
    )
    return TALK


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    print(text)
    if text.lower() == "привет":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="привет!")
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="ты дурак?"
        )


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
        a = random.randint(1,100)
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
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{a}?')
        context.user_data["a"] = a
    elif choise == "<":
        context.user_data["end"] = context.user_data["a"]
        a = random.randint(context.user_data["start"], context.user_data["end"])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{a}?")
        context.user_data["a"] = a
    elif choise == "Угадал!":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Угадал!")
        context.user_data["amount_games"] += 1
        context.user_data.pop('start')
        context.user_data.pop('end')
        context.user_data.pop('a')
        return await start(update,context)

# async def game_2(update: Update, context: ContextTypes.DEFAULT_TYPE):

if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(os.getenv('TOKEN'))
        .build()
    )
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("biba", biba),
                CommandHandler("info", info),
                CommandHandler("game", game_start),
                CallbackQueryHandler(talk_start, pattern='talk'),
                CallbackQueryHandler(game_start, pattern='game')
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, game)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Handler - обработчик
    application.add_handler(conv_handler)

    # & - И and
    # | - Или or
    # ~ - НЕ

    application.run_polling()