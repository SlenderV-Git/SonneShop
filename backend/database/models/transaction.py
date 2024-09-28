from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.models.base.core import Base
from backend.database.models.mixins import ModelWithIDMixin, ModelWithTimeMixin


class TransactionModel(ModelWithIDMixin, ModelWithTimeMixin, Base):
    __tablename__ = "transaction"

    credit_amount: Mapped[int] = mapped_column(nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))

    account: Mapped["AccountModel"] = relationship(back_populates="transactions")  # type: ignore # noqa: F821
