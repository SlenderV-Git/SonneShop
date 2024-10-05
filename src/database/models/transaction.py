from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base.core import Base
from src.database.models.mixins import ModelWithIDMixin, ModelWithTimeMixin


class TransactionModel(ModelWithIDMixin, ModelWithTimeMixin, Base):
    __tablename__ = "transaction"

    amount: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))
    approved: Mapped[bool] = mapped_column(default=False)

    account: Mapped["AccountModel"] = relationship(back_populates="transactions")  # type: ignore # noqa: F821
    user: Mapped["UserModel"] = relationship(back_populates="transactions")  # type: ignore # noqa: F821
