from aiogram.dispatcher.filters.state import State, StatesGroup


class Questionnaire(StatesGroup):
    team = State()
    team_interact = State()
    create_team = State()
    looking_team = State()
    join_team = State()

    contact = State()
    contact_data = State()
    sphere_work = State()
    sphere_work_other = State()
    vertical_work = State()
    vertical_work_other = State()
    steam_url = State()
    faceit_url = State()
    faceit_level = State()
