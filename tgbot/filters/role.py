from typing import Union

from aiogram.dispatcher.filters import BaseFilter



class Role_Filter(BaseFilter):
    """Filter for role of users."""
    user_role: Union[object, list]

    async def __call__(self, *args, **data) -> bool:
        if isinstance(self.user_role, object):
            return data["role"] == self.user_role
        else:
            return data["role"] in self.user_role
