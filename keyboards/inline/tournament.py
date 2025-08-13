from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_tournaments(tournaments: dict[int, str]):
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for id, name in tournaments.items():
        buttons.append(
            InlineKeyboardButton(text=name, callback_data=f'get_tournament_{id}'),
        )
    keyboard.add(*buttons)
    return keyboard


def get_tournament_keyboard(tournament_id) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='🔥 Участвовать', callback_data=f'join_tournament_{tournament_id}')
    keyboard.add(button)
    return keyboard
