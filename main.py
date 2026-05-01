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

if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [
                CommandHandler("game", game_start),
                CallbackQueryHandler(talk_start, pattern="^talk$"),
                CallbackQueryHandler(game_start, pattern="^game$"),
                CallbackQueryHandler(game_2_start, pattern="^game_2$"),
            ],
            TALK: [MessageHandler(filters.TEXT & ~filters.COMMAND, talk), CallbackQueryHandler(start, pattern="^start$")],
            GAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, game),],
            CITIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, game_2),CallbackQueryHandler(start, pattern="^start$")],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Handler - обработчик
    application.add_handler(conv_handler)

    # & - И and
    # | - Или or
    # ~ - НЕ

    application.run_polling()
