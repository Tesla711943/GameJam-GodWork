import asyncio
import logging
from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, MessageCallback, ButtonsPayload, CallbackButton
import sqlite3

logging.basicConfig(level=logging.INFO)


#=== Baza Dannix Podklucheniya === 
conn = sqlite3.connect("supportMeasures.db")
cursor = conn.cursor()

bot = Bot('f9LHodD0cOJS9bR1dR0a5Aq94uoVZ3Rsf6BcY73b6U_Mtx4hK1vhnp34Fv7kM9dU8KQSqzHsGUuyRV3tQekD')
dp = Dispatcher()

user_state = {}
chosen_strategy = {}  # {user_id: [status, direction]}


# === Главное меню с кнопками ===
async def show_main_menu(event):
    buttons = [
        [CallbackButton(text="Указать статус", payload="status")],
        [CallbackButton(text="Указать направление", payload="direction")],
        [CallbackButton(text="Посмотреть информацию", payload="info")]
    ]
    payload = ButtonsPayload(buttons=buttons).pack()
    await event.message.answer(
        "Выбери действие ниже ⬇",
        attachments=[payload]
    )


# === Кнопки для статуса и направления ===
async def show_status_buttons(event):
    buttons = [
        [CallbackButton(text="Молодой учёный", payload="status_молодой учёный")],
        [CallbackButton(text="Студент", payload="status_студент")],
        [CallbackButton(text="Аспирант", payload="status_аспирант")]
    ]
    payload = ButtonsPayload(buttons=buttons).pack()
    await event.message.answer("Выберите статус:", attachments=[payload])
    user_state[event.from_user.user_id] = "status_awaiting"


async def show_direction_buttons(event):
    buttons = [
        [CallbackButton(text="Техническое", payload="direction_техническое")],
        [CallbackButton(text="Медицинское", payload="direction_медицинское")],
        [CallbackButton(text="Аэрокосмическое", payload="direction_аэрокосмическое")],
        [CallbackButton(text="Гуманитарное", payload="direction_гуманитарное")],
        [CallbackButton(text="Естественное", payload="direction_естественное")]
    ]
    payload = ButtonsPayload(buttons=buttons).pack()
    await event.message.answer("Выберите направление:", attachments=[payload])
    user_state[event.from_user.user_id] = "direction_awaiting"


# === Старт бота ===
@dp.bot_started()
async def bot_started(event: BotStarted):
    buttons = [
        [CallbackButton(text="Старт", payload="hello")]
    ]
    payload = ButtonsPayload(buttons=buttons).pack()
    await event.bot.send_message(
        chat_id=event.chat_id,
        text="Начнём?",
        attachments=[payload]
    )


# === Обработка нажатий кнопок ===
@dp.message_callback()
async def on_callback(event: MessageCallback):
    data = event.callback.payload
    user_id = event.from_user.user_id

    if user_id not in chosen_strategy:
        chosen_strategy[user_id] = [None, None]

    # Старт и главное меню
    if data == "hello":
        user_state[user_id] = "main_menu"
        await show_main_menu(event)

    elif data == "status":
        await show_status_buttons(event)

    elif data.startswith("status_"):
        chosen_strategy[user_id][0] = data.split("_")[1]
        user_state[user_id] = "main_menu"
        await event.message.answer(f"Ваш статус — {chosen_strategy[user_id][0].capitalize()}")
        await show_main_menu(event)

    elif data == "direction":
        await show_direction_buttons(event)

    elif data.startswith("direction_"):
        chosen_strategy[user_id][1] = data.split("_")[1]
        user_state[user_id] = "main_menu"
        await event.message.answer(f"Ваше направление — {chosen_strategy[user_id][1].capitalize()}")
        await show_main_menu(event)

    elif data == "info":
        status, direction = chosen_strategy[user_id]
        status = status or "не установлен"
        direction = direction or "не установлено"
        await event.message.answer(
            f"Ваш статус: {status.capitalize()}\n"
            f"Ваше направление: {direction.capitalize()}"
        )

    else:
        await show_main_menu(event)


# === Запуск ===
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
