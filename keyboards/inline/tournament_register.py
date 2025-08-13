from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_agreement_keyboard(callback_data: str = 'agreement') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='✅ Принять', callback_data=callback_data)
    keyboard.add(button)
    return keyboard


def get_start_questionnaire_keyboard(callback_data: str = 'start_questionnaire') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='Отправить анкету', callback_data=callback_data)
    keyboard.add(button)
    return keyboard


def get_tournament_register_keyboard(callback_data: str = 'tournament_register') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='⚔️ Участвовать в турнире', callback_data=callback_data)
    keyboard.add(button)
    return keyboard


def get_sphere_work_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Баинг/соло', callback_data='sphere_work_buying_solo'),
        InlineKeyboardButton(text='Рекламодатель', callback_data='sphere_work_ad'),
        InlineKeyboardButton(text='Affiliate program', callback_data='sphere_work_ap'),
        InlineKeyboardButton(text='Медиа', callback_data='sphere_work_media'),
        InlineKeyboardButton(text='Другое', callback_data='sphere_work_other'),
    ]
    keyboard.add(*buttons)
    return keyboard


def get_vertical_work_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='IGaming', callback_data='vertical_work_buying_solo'),
        InlineKeyboardButton(text='Nutra', callback_data='vertical_work_ad'),
        InlineKeyboardButton(text='Crypto', callback_data='vertical_work_ap'),
        InlineKeyboardButton(text='Dating', callback_data='vertical_work_media'),
        InlineKeyboardButton(text='Другое', callback_data='vertical_work_other'),
    ]
    keyboard.add(*buttons)
    return keyboard


def get_team_interaction_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Создать команду', callback_data='create_team'),
        InlineKeyboardButton(text='Ищу команду', callback_data='looking_team'),
        InlineKeyboardButton(text='Присоединиться к команде', callback_data='join_team'),
    ]
    keyboard.add(*buttons)
    return keyboard
