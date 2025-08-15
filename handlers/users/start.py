from aiogram import types
from aiogram.utils.markdown import hlink
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, config
from keyboards.inline.tournament_register import get_agreement_keyboard, get_start_questionnaire_keyboard
from keyboards.inline.menu import get_menu_keyboard


@dp.message_handler(CommandStart(), state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.reset_state(with_data=True)

    registry_service = dp['registry_service']
    is_agreed = await registry_service.is_agreed(message.from_user.id)
    is_verified = await registry_service.is_verified(message.from_user.id)
    is_admin = await registry_service.is_admin(message.from_user.id)
    is_questioned = await registry_service.is_questioned(message.from_user.id)

    if is_admin or (is_questioned and is_agreed and is_verified):
        text = 'Меню:'
        reply_markup = get_menu_keyboard(channel_url=config.other.channel_url)
    elif not is_agreed:
        text = 'Ознакомьтесь с правилами турнира'
        if agreement_url := config.other.agreement_url:
            text = hlink(title=text, url=agreement_url)
        reply_markup = get_agreement_keyboard()
    elif not is_questioned:
        text = 'Добро пожаловать! Заполните анкету:'
        reply_markup = get_start_questionnaire_keyboard()
    else:
        text = 'Дождитесь проверки заявки'
        reply_markup = None

    await message.answer(text=text, reply_markup=reply_markup)


@dp.callback_query_handler(text='menu', state='*')
async def menu(call: types.CallbackQuery):
    text = 'Меню:'
    await call.message.edit_text(text=text, reply_markup=get_menu_keyboard(channel_url=config.other.channel_url))
