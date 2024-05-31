from asyncio import run, sleep
from os import getenv

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums.chat_action import ChatAction
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from sheet import get_sheet

load_dotenv()
TELEGRAM_BOT_TOKEN: str = getenv('TELEGRAM_BOT_TOKEN')
NAME_SHEET: list = getenv('NAME_SHEET')
JSON_SHEET: str = getenv('JSON_SHEET')

bot: Bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp: Dispatcher = Dispatcher()
router: Router = Router()
dp.include_router(router)


@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """Команда старт."""
    result: bool = await bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )

    msg = 'Сервисный бот приветствует тебя в Авто Гарант! Напиши что-нибудь и я тебе покажу список клиентов!'
    await message.answer(msg)


@router.message(F.content_type == 'text')
async def process_text_message(message: Message):
    """Принимает текстовые сообщения."""
    result: bool = await bot.send_chat_action(
        chat_id=message.from_user.id, action=ChatAction.TYPING
    )

    msg = f'Загружаю таблицу {NAME_SHEET}.sheet'
    await message.answer(text=msg)

    sheet = get_sheet(filename=JSON_SHEET, name_sheet=NAME_SHEET)
    clients, numbers, autos = (
        sheet.col_values(2),
        sheet.col_values(3),
        sheet.col_values(4),
    )

    for client, number, auto in zip(clients, numbers, autos):
        msg = f'Клиент: {client}\nНомер телефона: {number}\nАвтомобиль: {auto}'
        await message.answer(text=msg)
        await sleep(0.2)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
