from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery


class WithTeamFilter(BoundFilter):
    key = 'with_team'

    def __init__(self, dispatcher=None) -> None:
        self.registry_service = dispatcher['registry_service'] if dispatcher else None

    async def check(self, obj: Message | CallbackQuery) -> bool:
        from_user = getattr(obj, 'from_user', None)
        if from_user is None and hasattr(obj, 'message'):
            from_user = obj.message.from_user

        if from_user is None:
            return False

        is_verified = await self.registry_service.with_team(from_user.id)
        return is_verified
