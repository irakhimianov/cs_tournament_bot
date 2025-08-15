from datetime import datetime

from aiogram import types

from loader import dp, config
from keyboards.inline.tournament import (
    get_tournament_keyboard,
    get_tournaments
)
from keyboards.inline.menu import get_menu_keyboard
from keyboards.inline.back import get_back_keyboard


@dp.callback_query_handler(text='active_tournaments')
async def tournament(call: types.CallbackQuery) -> None:
    api_client = dp['api_client']
    response = await api_client.get_tournaments(params={'is_finished': False})
    if not response or not response.json().get('results', []):
        text = 'Нет активных турниров'
        return await call.message.edit_text(text=text, reply_markup=get_back_keyboard('menu'))

    text = 'Список активных турниров:'
    tournaments = response.json().get('results', [])
    data = {t.get('id'): t.get('name') for t in tournaments}
    await call.message.edit_text(text=text, reply_markup=get_tournaments(data))


@dp.callback_query_handler(text_contains='get_tournament_')
async def get_tournament(call: types.CallbackQuery) -> None:
    *_, tournament_id = call.data.split('_')

    api_client = dp['api_client']
    response = await api_client.get_tournament(tournament_id)
    data = response.json()
    name = data.get('name')

    await call.message.edit_text(text=name, reply_markup=get_tournament_keyboard(tournament_id))


@dp.callback_query_handler(text_contains='join_tournament_')
async def join_tournament(call: types.CallbackQuery):
    *_, tournament_id = call.data.split('_')

    api_client = dp['api_client']
    player_id = None
    players = await api_client.get_players(params={'telegram_id': call.from_user.id})
    if results := players.json().get('results', []):
        player_id = results[0].get('id')

    if tournament_id and player_id:
        response = await api_client.get_tournament_players(params={'tournament': tournament_id, 'player': player_id})
        if response and response.json().get('results', []):
            results = response.json().get('results', [])
            tournament_player = results[0]
            if not tournament_player.get('confirmed_at'):
                await api_client.edit_tournament_players(tournament_player.get('id'),
                                                         data={'confirmed_at': datetime.now()})
            text = '✅ Вы подтвердили участие в турнире'
            await call.answer(text=text, show_alert=True)
            await call.message.edit_text(text='Меню', reply_markup=get_menu_keyboard(channel_url=config.other.channel_url))
            return
        elif response and not response.json().get('results', []):
            await api_client.create_tournament_players(data={'tournament': tournament_id, 'player': player_id, 'confirmed_at': datetime.now()})
            text = '✅ Вы подтвердили участие в турнире'
            await call.answer(text=text, show_alert=True)
            await call.message.edit_text(text='Меню', reply_markup=get_menu_keyboard(channel_url=config.other.channel_url))
            return

    await call.message.edit_text(text='Что-то пошло не так...', reply_markup=get_back_keyboard('menu'))
