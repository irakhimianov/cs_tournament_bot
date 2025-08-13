from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, dispatcher=None) -> None:
        self.registry_service = dispatcher['registry_service']

    async def check(self, obj: Message | CallbackQuery) -> bool:
        from_user = getattr(obj, 'from_user', None)
        if from_user is None and hasattr(obj, 'message'):
            from_user = obj.message.from_user

        if from_user is None:
            return False

        is_admin = await self.registry_service.is_admin(from_user.id)
        return is_admin
