from aiogram.dispatcher.filters.state import State, StatesGroup


class Broadcast(StatesGroup):
    text = State()


class BroadcastTournament(StatesGroup):
    text = State()


class TeamMessage(StatesGroup):
    first_team = State()
    second_team = State()
    text = State()
