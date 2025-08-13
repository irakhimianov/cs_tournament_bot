from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.cancel import get_cancel_button


def get_admin_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='📢 Создать рассылку', callback_data='admin_broadcast'),
        InlineKeyboardButton(text='🏆 Объявление о турнире', callback_data='admin_tournament'),
        InlineKeyboardButton(text='💬 Написать двум командам', callback_data='admin_send_team_message'),
    ]
    keyboard.add(*buttons)
    return keyboard


def get_tournaments(tournaments: dict[int, str]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for id, name in tournaments.items():
        buttons.append(
            InlineKeyboardButton(text=name, callback_data=f'admin_get_tournament_{id}'),
        )
    keyboard.add(*buttons)
    return keyboard


def team_inline_query_keyboard(text: str, inline_text: str):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text=text, switch_inline_query_current_chat=inline_text),
        get_cancel_button(),
    ]

    keyboard.add(*buttons)
    return keyboard
