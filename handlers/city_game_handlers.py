from telegram import (
    Update,
)
from telegram.ext import (
    ContextTypes,
)
from openai import OpenAI

from config.states import CITIES


async def game_2_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "developer",
                "content": "ты бот в телеграмме, который играет с человеком в города. Назови рандомный город В ответе напиши только город. Ничего кроме города не пиши.",
            },
            # {"role": "user", "content": text},
        ],
    )
    context.user_data["city"] = response.output_text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Вы попали в игру города \nЯ начинаю, {response.output_text}",
    )
    return CITIES


async def game_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_city = update.effective_message.text
    bot_city = context.user_data["city"]
    print("Город человека", user_city)
    print("Город ИИ", bot_city)
    lb = bot_city[-1]
    if lb == "ь":
        lb = bot_city[-2]
    if lb != user_city[0].lower():
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Я сказал {bot_city}, значит тебе нужно вспомнить город на {bot_city[-1]}",
        )
        return CITIES
    # задать вопрос чату гпт, ответь да или нет. Существует ли город и дать город человека. Если да то идем дальше, если нет, то пишем что я не знаю такой город
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "developer",
                "content": "ты бот в телеграмме, который играет с человеком в города. Назови следующий город на букву, на которую заканчивается город человека. В ответе пиши только город, без лишнего текста.",
            },
            {"role": "user", "content": user_city},
        ],
    )
    bot_city = response.output_text.strip()
    context.user_data["city"] = bot_city

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_city,
    )