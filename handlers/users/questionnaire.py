from datetime import datetime

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ContentType

import consts
import states
from loader import dp
from keyboards.inline.cancel import get_cancel_keyboard
from keyboards.inline.tournament_register import (
    get_start_questionnaire_keyboard,
    get_sphere_work_keyboard,
    get_vertical_work_keyboard,
    get_team_interaction_keyboard,
    get_agreement_keyboard,
)
from keyboards.reply.tournament_register import get_contact_keyboard


@dp.callback_query_handler(text='agreement')
async def cmd_agreement(call: types.CallbackQuery) -> None:
    api_client = dp['api_client']
    data = {'telegram_id': call.from_user.id, 'agreed_at': datetime.now()}
    if username := call.from_user.username:
        data |= {'telegram_username': username}
    resp = await api_client.create_player(data=data)
    if not resp:
        text = 'Что-то пошло не так, попробуйте еще раз'
        reply_markup = get_agreement_keyboard()
    else:
        text = 'Добро пожаловать! Заполните анкету:'
        reply_markup = get_start_questionnaire_keyboard()
    await call.message.edit_text(text=text, reply_markup=reply_markup)


@dp.callback_query_handler(text='start_questionnaire')
async def questionnaire_name(call: types.CallbackQuery):
    if not call.from_user.username:
        await states.Questionnaire.contact.set()
    else:
        await states.Questionnaire.team.set()

    text = 'Ваше имя:'
    await call.message.edit_text(text=text)


@dp.message_handler(state=states.Questionnaire.contact)
async def questionnaire_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    text = 'Отправьте контактные данные'
    await message.answer(text=text, reply_markup=get_contact_keyboard())
    await states.Questionnaire.contact_data.set()


@dp.message_handler(state=states.Questionnaire.team)
async def questionnaire_team(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    text = 'Есть ли CS команда?'
    await message.answer(text=text, reply_markup=get_team_interaction_keyboard())
    await states.Questionnaire.team_interact.set()


@dp.callback_query_handler(text='create_team', state=states.Questionnaire.team_interact)
async def questionnaire_team_interact_create(call: types.CallbackQuery):
    text = 'Введите название команды'
    await call.message.edit_text(text=text)
    await states.Questionnaire.create_team.set()


@dp.message_handler(state=states.Questionnaire.create_team)
async def questionnaire_create_team(message: types.Message):
    api_client = dp['api_client']
    name = message.text
    resp = await api_client.get_teams(params={'name': name})
    if resp.json().get('results'):
        text = 'Команда с таким именем уже существует. Придумайте другое имя'
        await message.answer(text=text)
        return

    player_id = None
    players = await api_client.get_players(params={'telegram_id': message.from_user.id})
    if results := players.json().get('results', []):
        player_id = results[0].get('id')

    if player_id:
        await api_client.create_team(data={'name': name, 'created_by': player_id})

    text = 'С чем вы работаете?'
    await message.answer(text=text, reply_markup=get_sphere_work_keyboard())
    await states.Questionnaire.sphere_work.set()


@dp.callback_query_handler(text='join_team', state=states.Questionnaire.team_interact)
async def questionnaire_team_interact_join(call: types.CallbackQuery):
    text = (
        'Уточните у создателя команды пригласительный код. Найти пригласительный код можно в главном меню - '
        'кнопка о команде и отправьте его следующим сообщением. Например, код: 123456'
    )
    await call.message.edit_text(text=text)
    await states.Questionnaire.join_team.set()


@dp.message_handler(state=states.Questionnaire.join_team)
async def questionnaire_join_team(message: types.Message):
    api_client = dp['api_client']
    resp = await api_client.get_teams(params={'invite_code': message.text})
    if not resp or not resp.json().get('results'):
        text = 'Команда с таким пригласительным кодом не найдена. Попробуйте ввести другой код:'
        await message.answer(text=text)
        return

    team_id = None
    team = resp.json().get('results', [])
    if team:
        team_id = team[0].get('id')

    player_id = None
    players = await api_client.get_players(params={'telegram_id': message.from_user.id})
    if results := players.json().get('results', []):
        player_id = results[0].get('id')

    if team_id and player_id:
        await api_client.add_team_player(team_id, data={'player': player_id})
    text = 'С чем вы работаете?'
    await message.answer(text=text, reply_markup=get_sphere_work_keyboard())
    await states.Questionnaire.sphere_work.set()


@dp.callback_query_handler(text='looking_team', state=states.Questionnaire.team_interact)
async def questionnaire_looking_team(call: types.CallbackQuery):
    text = 'С чем вы работаете?'
    await call.message.edit_text(text=text, reply_markup=get_sphere_work_keyboard())
    await states.Questionnaire.sphere_work.set()


@dp.message_handler(content_types=ContentType.CONTACT, state=states.Questionnaire.contact_data)
async def questionnaire_message_team_interact(message: types.Message, state: FSMContext):
    if contact := message.contact:
        async with state.proxy() as data:
            data['contact'] = contact.phone_number

    text = 'Есть ли CS команда?'
    await message.answer(text=text, reply_markup=get_team_interaction_keyboard())
    await states.Questionnaire.team_interact.set()


@dp.callback_query_handler(text_contains='sphere_work_', state=states.Questionnaire.sphere_work)
async def questionnaire_sphere_work(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'sphere_work_other':
        text = 'Введите с чем вы работаете:'
        reply_markup = get_cancel_keyboard()
        await states.Questionnaire.sphere_work_other.set()
    else:
        text = 'С какой вертикалью вы работаете?'
        reply_markup = get_vertical_work_keyboard()
        await states.Questionnaire.vertical_work.set()
        async with state.proxy() as data:
            data['sphere_work'] = consts.sphere_work_choices.get(call.data, '')

    await call.message.edit_text(text=text, reply_markup=reply_markup)


@dp.message_handler(state=states.Questionnaire.sphere_work_other)
async def questionnaire_sphere_work_other(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sphere_work'] = f'Другое: {message.text}'

    text = 'С какой вертикалью вы работаете?'
    await message.answer(text=text, reply_markup=get_vertical_work_keyboard())
    await states.Questionnaire.vertical_work.set()


@dp.callback_query_handler(text_contains='vertical_work_', state=states.Questionnaire.vertical_work)
async def questionnaire_vertical_work(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'vertical_work_other':
        text = 'Введите с какой вертикалью вы работаете:'
        await states.Questionnaire.vertical_work_other.set()
    else:
        text = 'Ссылка на Steam профиль:'
        await states.Questionnaire.steam_url.set()
        async with state.proxy() as data:
            data['vertical_work'] = consts.vertical_work_choices.get(call.data, '')

    await call.message.edit_text(text=text)


@dp.message_handler(state=states.Questionnaire.vertical_work_other)
async def questionnaire_vertical_work_other(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vertical_work'] = f'Другое: {message.text}'
    text = 'Ссылка на Steam профиль:'
    await message.answer(text=text)
    await states.Questionnaire.steam_url.set()


@dp.message_handler(state=states.Questionnaire.steam_url)
async def questionnaire_steam_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['steam_url'] = message.text
    text = 'Ссылка на FaceIT:'
    await message.answer(text=text)
    await states.Questionnaire.faceit_url.set()


@dp.message_handler(state=states.Questionnaire.faceit_url)
async def questionnaire_faceit_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['faceit_url'] = message.text
    text = 'Уровень на FaceIT:'
    await message.answer(text=text)
    await states.Questionnaire.faceit_level.set()


@dp.message_handler(state=states.Questionnaire.faceit_level)
async def questionnaire_faceit_level(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        text = 'Некорректное значение. Допускаются числовые значения. Попробуйте еще раз'
        return await message.answer(text=text)

    async with state.proxy() as data:
        data['faceit_level'] = message.text
        request_data = {k: v for k, v in data.items()}

    api_client = dp['api_client']
    player_id = None
    players = await api_client.get_players(params={'telegram_id': message.from_user.id})
    if results := players.json().get('results', []):
        player_id = results[0].get('id')

    if player_id:
        request_data |= {'questioned_at': datetime.now()}
        await api_client.edit_player(player_id=player_id, data=request_data)

    text = 'Анкета отправлена на проверку'
    await message.answer(text=text)
    await state.finish()
