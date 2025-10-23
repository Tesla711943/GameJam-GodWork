import asyncio
import logging
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
async def a(event: MessageCreated):
    if MessageCreated == "Студент":
       await event.message.answer("ты студент")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
