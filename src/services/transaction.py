from typing import Sequence
from src.common.exceptions.services import NotFoundError
from src.common.dto.transaction import Transaction, TransactionSchema
from src.common.interfaces.gateway import BaseGateway
from src.database.repositories.transaction import TransactionRepostory
from src.database.converter import from_model_to_dto, from_list_model_to_list_dto


class TransactionService(BaseGateway):
    __slots__ = "_repository"

    def __init__(self, repository: TransactionRepostory) -> None:
        self._repository = repository

    async def create(self, user_id: int, data: Transaction) -> TransactionSchema:
        return from_model_to_dto(
            await self._repository.create(user_id, data), TransactionSchema
        )

    async def approve(self, transaction_id: int) -> Transaction:
        transaction = await self._repository.update(
            transaction_id=transaction_id, approved=True
        )
        if not transaction:
            raise NotFoundError("Transaction not found or paid is approved")
        return from_model_to_dto(transaction, Transaction)

    async def get_all(
        self, user_id: int, offset: int = None, limit: int = None
    ) -> Sequence[Transaction]:
        transactions = await self._repository.get_all(user_id, offset, limit)
        return from_list_model_to_list_dto(transactions, Transaction)
