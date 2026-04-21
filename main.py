import logging
from telegram import (
    Update,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
)
import os
from dotenv import load_dotenv

from handlers.city_game_handlers import game_2, game_2_start

from handlers.game_handler import game, game_start
from handlers.talk_handler import talk, talk_start

from  config.states import CITIES, GAME, TALK, MAINMENU
from handlers.start_handler import start

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


# callback

async def biba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="боба")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.effective_user
    )



if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("biba", biba),
                CommandHandler("info", info),
                CommandHandler("game", game_start),
                CallbackQueryHandler(talk_start, pattern="^talk$"),
                CallbackQueryHandler(game_start, pattern="^game$"),
                CallbackQueryHandler(game_2_start, pattern="^game_2$"),
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk)],
            GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, game)],
            CITIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, game_2)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Handler - обработчик
    application.add_handler(conv_handler)

    # & - И and
    # | - Или or
    # ~ - НЕ

    application.run_polling()
