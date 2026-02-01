from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from asyncio import run

import functions

BOT_TOKEN = "6057315603:AAHxnkglSCHpKkXji6KYYhlAJ7PX_KIuWYw"


async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Start handler
    dp.message.register(functions.start_handler, CommandStart())

    # FSM handlers
    dp.message.register(functions.phone_handler, functions.UserForm.phone)
    dp.message.register(functions.fullname_handler, functions.UserForm.fullname)
    dp.message.register(functions.age_handler, functions.UserForm.age)
    dp.message.register(functions.region_handler, functions.UserForm.region)
    dp.message.register(functions.district_handler, functions.UserForm.district)


    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
