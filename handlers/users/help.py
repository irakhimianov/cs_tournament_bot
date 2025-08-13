from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from keyboards.inline.back import get_back_keyboard


@dp.message_handler(CommandHelp(), state='*')
async def cmd_help(message: types.Message):
    text = 'По всем вопросам обращаться в техподдержку'
    await message.answer(text=text)


@dp.callback_query_handler(text='help')
async def call_help(call: types.CallbackQuery):
    text = 'По всем вопросам обращаться в техподдержку'
    await call.message.edit_text(text=text, reply_markup=get_back_keyboard('menu'))
