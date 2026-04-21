from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from openai import OpenAI

from  config.states import TALK


async def talk_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Вы попали в режим разговора! Напишите что-то и бот вам ответит",
    )
    context.user_data["prev_messages"] = []
    return TALK


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    print(text)
    if text.lower() == "привет":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="привет!")
    else:
        client = OpenAI()
        if len(context.user_data["prev_messages"]) >= 6:
            context.user_data["prev_messages"].pop(0)
            context.user_data["prev_messages"].pop(0)
        response = client.responses.create(
            model="gpt-5-mini",
            input=[
                {
                    "role": "developer",
                    "content": "ты бот в телеграмме, отвечай на вопросы человека. Говори с человекам как будто он не делает твою домашку, которую ты ему задаешь ",
                }
            ]
            + context.user_data["prev_messages"]
            + [
                {"role": "user", "content": text},
            ],
        )
        context.user_data["prev_messages"].append({"role": "user", "content": text})
        context.user_data["prev_messages"].append(
            {"role": "assistant", "content": response.output_text}
        )

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=response.output_text
        )