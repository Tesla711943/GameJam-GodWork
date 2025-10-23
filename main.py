import asyncio
import logging
import maxapi
from maxapi.filters import F
from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, Command, MessageCreated

logging.basicConfig(level=logging.INFO)

bot = Bot('f9LHodD0cOJS9bR1dR0a5Aq94uoVZ3Rsf6BcY73b6U_Mtx4hK1vhnp34Fv7kM9dU8KQSqzHsGUuyRV3tQekD')
dp = Dispatcher()


@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='Привет! Отправь мне /start'
    )

@dp.message_created(Command('start'))
async def hello(event: MessageCreated):
    await event.message.answer("Привет! Напиши /status или /direction")

user_state = {}
# {userid:[1, 2]}
chosen_strategy = {}


@dp.message_created(Command('status'))
async def ask_status(event: MessageCreated):
    user_id = event.from_user.user_id
    await event.message.answer(
        "Выберите один из вариантов: Молодой учёный, Студент, Аспирант"
    )
    user_state[user_id] = "status_awaiting"

    
@dp.message_created()
async def handle_message(event: MessageCreated):

    user_id = event.from_user.user_id
    if user_state[user_id] == "status_awaiting":
        text = event.message.body.text.strip().lower()
        if text == "студент":
            user_state[user_id] = ""
            await event.message.answer("Ваш статус - Студент")
            chosen_strategy[user_id] = ["Студент", ""]
        elif text == "аспирант":
            user_state[user_id] = ""
            await event.message.answer("Ваш статус - Аспирант")
            chosen_strategy[user_id] = ["Аспирант", ""]
        elif text == "молодой учёный":
            user_state[user_id] = ""
            await event.message.answer("Ваш статус - Молодой Учёный")
            chosen_strategy[user_id] = ["Молодой Учёный", ""]
        else:
            await event.message.answer("Пожалуйста, введите один из возможных статусов")
    else:
        await event.message.answer("Введите /status для установки статуса")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
