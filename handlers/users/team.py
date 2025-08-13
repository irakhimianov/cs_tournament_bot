from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from keyboards.inline.menu import get_menu_keyboard
from keyboards.inline.back import get_back_keyboard


@dp.callback_query_handler(text='about_team')
async def about_team(call: types.CallbackQuery):
    api_client = dp['api_client']
    response = await api_client.get_players(params={'telegram_id': call.from_user.id})

    reply_markup = get_back_keyboard('menu')

    if not response or not response.json().get('results', []):
        text = 'Команды не найдены'
        return await call.message.edit_text(text=text, reply_markup=reply_markup)

    text = ''
    player = response.json().get('results', [{}])[0]
    teams = player.get('teams', [])
    if not teams:
        text = 'Команды не найдены'
        return await call.message.edit_text(text=text, reply_markup=reply_markup)

    for team in teams:
        text += f'Название: <b>{team.get("name")}</b>\nПригласительный код: <code>{team.get("invite_code")}</code>\n\n'

    await call.message.edit_text(text=text.strip(), reply_markup=reply_markup)
