from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from openai import OpenAI

from config.states import GADALKA

async def gadalka_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Я предсказыватель,напиши свой вопрос и я дам ответ')
     
    return GADALKA

async def gadalka(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_message.text
    
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-nano",
        input=[
            {
                "role": "developer",
                "content": "ты бот в телеграмме, давай краткие ответы человеку в стиле шарика с предсказаниями.",
            },
            {"role": "user", "content": user},
        ],
    )
    bot = response.output_text.strip()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot
    )