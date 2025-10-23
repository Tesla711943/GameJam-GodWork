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

@dp.message_created(Command('status'))
async def ask_status(event: MessageCreated):
    await event.message.answer(
        "Выберите один из вариантов: Молодой учёный, Студент, Аспирант"
    )
    
@dp.message_created()
async def handle_message(event: MessageCreated):
    text = event.message.body.text.strip().lower()
    if text == "студент":
        await event.message.answer("Ваш статус - Студент")
    elif text == "аспирант":
        await event.message.answer("Ваш статус - Аспирант")
    elif text == "молодой учёный":
        await event.message.answer("Ваш статус - Молодой Учёный")
    else:
        await event.message.answer("Пожалуйста, введите один из возможных статусов")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
