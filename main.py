import asyncio
import logging
from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, Command, MessageCreated

logging.basicConfig(level=logging.INFO)

bot = Bot('f9LHodD0cOJS9bR1dR0a5Aq94uoVZ3Rsf6BcY73b6U_Mtx4hK1vhnp34Fv7kM9dU8KQSqzHsGUuyRV3tQekD')
dp = Dispatcher()

user_state = {}
chosen_strategy = {}  # {user_id: [status, direction]}

@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.send_message(chat_id=event.chat_id, text='Привет! Отправь мне /start')

@dp.message_created(Command('start'))
async def hello(event: MessageCreated):
    await event.message.answer("Привет! Напиши /status или /direction")

# /status
@dp.message_created(Command('status'))
async def ask_status(event: MessageCreated):
    user_id = event.from_user.user_id
    await event.message.answer("Выберите один из вариантов: Молодой учёный, Студент, Аспирант")
    user_state[user_id] = "status_awaiting"


# /info
@dp.message_created(Command('info'))
async def show_info(event: MessageCreated):
    user_id = event.from_user.user_id
    data = chosen_strategy.get(user_id, [None, None])
    status = data[0] or "не установлен"
    direction = data[1] or "не установлено"

    await event.message.answer(
        f"Ваш статус: {status.capitalize()}\n"
        f"Ваше направление: {direction.capitalize()}"
    )

# /direction
@dp.message_created(Command('direction'))
async def ask_direction(event: MessageCreated):
    user_id = event.from_user.user_id
    await event.message.answer(
        "Выберите одно из направлений образования:\n"
        "Техническое, Медицинское, Аэрокосмическое, Гуманитарное, Естественное"
    )
    user_state[user_id] = "direction_awaiting"


@dp.message_created()
async def handle_message(event: MessageCreated):
    user_id = event.from_user.user_id
    text = event.message.body.text.strip().lower()

    # гарантируем, что у пользователя уже есть структура данных
    if user_id not in chosen_strategy:
        chosen_strategy[user_id] = [None, None]  # [status, direction]

    # обработка статуса
    if user_state.get(user_id) == "status_awaiting":
        if text in ["студент", "аспирант", "молодой учёный", "молодойучёный"]:
            chosen_strategy[user_id][0] = text  # записываем статус в 0-й элемент
            user_state[user_id] = ""
            await event.message.answer(f"Ваш статус — {text.capitalize()}")
        else:
            await event.message.answer("Пожалуйста, введите один из возможных статусов.")

    # обработка направления
    elif user_state.get(user_id) == "direction_awaiting":
        if text in ["техническое", "медицинское", "аэрокосмическое", "гуманитарное", "естественное"]:
            chosen_strategy[user_id][1] = text  # записываем направление в 1-й элемент
            user_state[user_id] = ""
            await event.message.answer(f"Ваше направление — {text.capitalize()}")
        else:
            await event.message.answer("Введите одно из предложенных направлений.")

    else:
        await event.message.answer("Введите /status или /direction для начала.")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
