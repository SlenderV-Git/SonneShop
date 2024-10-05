from typing import Optional, Sequence, Type


from src.common.dto.transaction import Tran
from src.database.models.transaction import TransactionModel
from src.database.repositories.base import BaseRepository


class TransactionRepostory(BaseRepository):
    __slots__ = ()

    @property
    def model(self) -> Type[TransactionModel]:
        return TransactionModel
