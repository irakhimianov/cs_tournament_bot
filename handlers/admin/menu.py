import asyncio
import hashlib
import random

from aiogram import types
from aiogram.types import ContentTypes

import states
from loader import dp, bot
from keyboards.inline.admin import get_admin_keyboard, get_tournaments, team_inline_query_keyboard
from keyboards.inline.cancel import get_cancel_keyboard
from keyboards.inline.tournament import get_tournament_keyboard


async def _copy_once(
        src_chat_id: int,
        message_id: int,
        dst_chat_id: int,
        disable_notification: bool = False,
        reply_markup = None,
) -> bool:
    try:
        await bot.copy_message(
            chat_id=dst_chat_id,
            from_chat_id=src_chat_id,
            message_id=message_id,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
        )
        return True
    except Exception as e:
        print(e)
        return False


@dp.message_handler(commands=['admin'])
async def cmd_admin(message: types.Message):
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(message.from_user.id)

    if not is_admin:
        return
    text = '👮‍ Админ-меню:'
    await message.answer(text=text, reply_markup=get_admin_keyboard())


@dp.callback_query_handler(text='admin', chat_type='private')
async def call_admin(call: types.CallbackQuery) -> None:
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(call.from_user.id)

    if not is_admin:
        return

    text = '👮‍ Админ-меню:'
    await call.message.edit_text(text=text, reply_markup=get_admin_keyboard())


@dp.callback_query_handler(text='admin_broadcast')
async def broadcast(call: types.CallbackQuery) -> None:
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(call.from_user.id)

    if not is_admin:
        return

    text = 'Введите сообщение для рассылки'
    await call.message.edit_text(text=text, reply_markup=get_cancel_keyboard())
    await states.Broadcast.text.set()


@dp.message_handler(state=states.Broadcast.text, content_types=ContentTypes.ANY)
async def broadcast_text(message: types.Message, state) -> None:
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(message.from_user.id)

    if not is_admin:
        return

    if message.media_group_id:
        await message.reply("Для рассылки пришлите одно фото/видео/медиа")
        return

    api_client = dp['api_client']
    response = await api_client.get_players(
        params={'is_verified': True, 'with_team': True, 'is_agreed': True, 'per_page': 1000}
    )
    if not response:
        await message.answer(text=f'Нет подходящих игроков для рассылки', reply_markup=get_admin_keyboard())
        return

    count = 0
    players = response.json().get('results', [])
    for player in players:
        try:
            result = await _copy_once(
                src_chat_id=message.chat.id,
                message_id=message.message_id,
                dst_chat_id=int(player.get('telegram_id')),
            )
            if result:
                count += 1
            await asyncio.sleep(1 + random.randint(0, 5))
        except Exception as e:
            continue

    await state.finish()
    await message.answer(text=f'Совершена рассылка по {count} пользователям', reply_markup=get_admin_keyboard())


@dp.callback_query_handler(text='admin_tournament')
async def admin_tournament(call: types.CallbackQuery) -> None:
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(call.from_user.id)

    if not is_admin:
        return

    api_client = dp['api_client']
    response = await api_client.get_tournaments(params={'is_finished': False})
    if not response:
        text = 'Нет активных турниров'
        await call.message.edit_text(text=text, reply_markup=get_admin_keyboard())
        return

    text = 'Список активных турниров для рассылки:'
    tournaments = response.json().get('results', [])
    data = {t.get('id'): t.get('name') for t in tournaments}
    await call.message.edit_text(text=text, reply_markup=get_tournaments(data))


@dp.callback_query_handler(text_contains='admin_get_tournament_')
async def admin_get_tournament_message(call: types.CallbackQuery, state) -> None:
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(call.from_user.id)

    if not is_admin:
        return

    *_, tournament_id = call.data.split('_')
    async with state.proxy() as data:
        data['tournament_id'] = tournament_id

    text = 'Введите сообщение к турниру для рассылки'
    await call.message.edit_text(text=text, reply_markup=get_cancel_keyboard())
    await states.BroadcastTournament.text.set()


@dp.message_handler(state=states.BroadcastTournament.text, content_types=ContentTypes.ANY)
async def broadcast_tournament_text(message: types.Message, state) -> None:
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(message.from_user.id)

    if not is_admin:
        return

    if message.media_group_id:
        await message.reply("Для рассылки пришлите одно фото/видео/медиа")
        return

    async with state.proxy() as data:
        tournament_id = data['tournament_id']

    api_client = dp['api_client']
    response = await api_client.get_players(
        params={'is_verified': True, 'with_team': True, 'is_agreed': True, 'per_page': 1000}
    )
    if not response:
        await message.answer(text=f'Нет подходящих игроков для рассылки', reply_markup=get_admin_keyboard())
        return

    reply_markup = get_tournament_keyboard(tournament_id)
    count = 0
    players = response.json().get('results', [])
    for player in players:
        try:
            result = await _copy_once(
                src_chat_id=message.chat.id,
                message_id=message.message_id,
                dst_chat_id=int(player.get('telegram_id')),
                reply_markup=reply_markup,
            )
            if result:
                count += 1
            await asyncio.sleep(1 + random.randint(0, 5))
        except Exception as e:
            continue

    await state.finish()
    await message.answer(text=f'Совершена рассылка по {count} пользователям', reply_markup=get_admin_keyboard())


@dp.callback_query_handler(text='admin_send_team_message')
async def admin_send_team_message(call: types.CallbackQuery) -> None:
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(call.from_user.id)

    if not is_admin:
        return

    text = 'Поиск команды по имени'
    await call.message.edit_text(
        text=text,
        reply_markup=team_inline_query_keyboard('Выбор первой команды', 'Первая команда: ')
    )
    await states.TeamMessage.first_team.set()


@dp.inline_handler(text_contains='Первая команда:', state=states.TeamMessage.first_team)
async def inline_first_team(inline_query: types.InlineQuery, state):
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(inline_query.from_user.id)

    if not is_admin:
        return

    api_client = dp['api_client']

    text = ''
    if query := inline_query.query:
        *_, text = query.split('Первая команда:')
        text = text.strip()

    items = []
    teams = []
    resp = await api_client.get_teams(params={'name': text, 'per_page': 1000})
    if results := resp.json().get('results', []):
        teams = [(r.get('id'), r.get('name')) for r in results]

    for team_id, team in teams:
        result_id = hashlib.md5((text + f'{team_id}').encode()).hexdigest()
        items.append(
            types.InlineQueryResultArticle(
                id=result_id,
                title=team,
                hide_url=True,
                input_message_content=types.InputTextMessageContent(f'#{team_id} {team}')
            )
        )

    await bot.answer_inline_query(
        inline_query_id=inline_query.id,
        results=items[:50],
        cache_time=10,
    )


@dp.inline_handler(text_contains='Вторая команда:', state=states.TeamMessage.second_team)
async def inline_second_team(inline_query: types.InlineQuery, state):
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(inline_query.from_user.id)

    if not is_admin:
        return

    api_client = dp['api_client']

    text = ''
    if query := inline_query.query:
        *_, text = query.split('Вторая команда:')
        text = text.strip()

    items = []
    teams = []
    resp = await api_client.get_teams(params={'name': text, 'per_page': 1000})
    if results := resp.json().get('results', []):
        teams = [(r.get('id'), r.get('name')) for r in results]

    for team_id, team in teams:
        result_id = hashlib.md5((text + f'{team_id}').encode()).hexdigest()
        items.append(
            types.InlineQueryResultArticle(
                id=result_id,
                title=team,
                hide_url=True,
                input_message_content=types.InputTextMessageContent(f'#{team_id} {team}')
            )
        )

    await bot.answer_inline_query(
        inline_query_id=inline_query.id,
        results=items[:50],
        cache_time=10,
    )


@dp.message_handler(state=states.TeamMessage.first_team)
async def first_team_message(message: types.Message, state):
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(message.from_user.id)

    if not is_admin:
        return

    if not message.via_bot:
        return

    text, _ = message.text.split()
    first_team_id = text.replace('#', '')
    async with state.proxy() as data:
        data['first_team_id'] = first_team_id

    text = 'Поиск команды по имени'
    await message.answer(text=text, reply_markup=team_inline_query_keyboard('Выбор второй команды', 'Вторая команда:'))
    await states.TeamMessage.second_team.set()


@dp.message_handler(state=states.TeamMessage.second_team)
async def second_team_message(message: types.Message, state):
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(message.from_user.id)

    if not is_admin:
        return

    if not message.via_bot:
        return

    text, _ = message.text.split()
    second_team_id = text.replace('#', '')
    async with state.proxy() as data:
        data['second_team_id'] = second_team_id

    text = 'Введите сообщение для рассылки'
    await message.answer(text=text, reply_markup=get_cancel_keyboard())
    await states.TeamMessage.text.set()


@dp.message_handler(state=states.TeamMessage.text)
async def broadcast_team_message_text(message: types.Message, state) -> None:
    registry_service = dp['registry_service']
    is_admin = await registry_service.is_admin(message.from_user.id)

    if not is_admin:
        return

    async with state.proxy() as data:
        second_team_id = data['second_team_id']
        first_team_id = data['first_team_id']

    await state.finish()

    api_client = dp['api_client']
    players = []
    response = await api_client.get_players(
        params={'team': first_team_id, 'is_agreed': True, 'per_page': 1000}
    )
    data = response.json().get('results', [])
    for d in data:
        players.append(d.get('telegram_id'))

    response = await api_client.get_players(
        params={'team': second_team_id, 'is_agreed': True, 'per_page': 1000}
    )
    data = response.json().get('results', [])
    for d in data:
        players.append(d.get('telegram_id'))

    if not players:
        await message.answer(text=f'Нет подходящих игроков для рассылки', reply_markup=get_admin_keyboard())
        return

    count = 0
    for player in players:
        try:
            result = await _copy_once(
                src_chat_id=message.chat.id,
                message_id=message.message_id,
                dst_chat_id=int(player),
            )
            if result:
                count += 1
            await asyncio.sleep(1 + random.randint(0, 5))
        except Exception as e:
            continue

    await state.finish()
    await message.answer(text=f'Совершена рассылка по {count} пользователям', reply_markup=get_admin_keyboard())
