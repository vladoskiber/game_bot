from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
)



from  config.states import MAINMENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update - полная инфа о том, что произошло
    # update.effective_user - полная инфа о человеке
    # update.effective_chat - полная инфа о чате
    #  update.effective_message - полная инфа о сообщении
    query = update.callback_query
    if query:
        await query.answer()
        await query.delete_message()

    if "amount_games" not in context.user_data:
        context.user_data["amount_games"] = 0
    keyboard = [
        [InlineKeyboardButton("Режим разговора", callback_data="talk")],
        [InlineKeyboardButton("Игра города", callback_data="game_2")],
        [InlineKeyboardButton("Игра загадай число", callback_data="game")],
    ]

    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"привет,{update.effective_user.first_name}\n\nУ тебя {context.user_data['amount_games']} игр(а)\n\nВ моем боте есть функции:\n"
        + "\nинформация о вас {update.effective_user}",
        reply_markup=markup,
    )

    return MAINMENU