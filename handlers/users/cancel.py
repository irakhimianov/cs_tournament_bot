from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot


@dp.callback_query_handler(text='cancel', state='*')
async def call_cancel(call: types.CallbackQuery, state: FSMContext) -> None:
    try:
        await state.finish()
    except:
        pass

    await bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )

    text = '❌<b>Последняя операция отменена</b>'
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
    )
    await call.answer()


@dp.message_handler(commands='cancel', state='*')
@dp.message_handler(text='❌ Отмена', state='*')
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    try:
        await state.finish()
    except:
        pass
    text = '❌<b>Последняя операция отменена</b>'
    await bot.send_message(chat_id=message.chat.id, text=text)
