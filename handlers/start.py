from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from misc.keyboards import main_kb


router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот для проведения опроса. Нажми 'Анкета', чтобы начать.", reply_markup=main_kb)
