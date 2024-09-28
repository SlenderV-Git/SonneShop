from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.models.base.core import Base
from backend.database.models.mixins import ModelWithIDMixin


class AccountModel(ModelWithIDMixin, Base):
    __tablename__ = "account"

    balance: Mapped[int] = mapped_column(default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["UserModel"] = relationship(back_populates="accounts")  # type: ignore # noqa: F821
    transactions: Mapped["TransactionModel"] = relationship(back_populates="account")  # type: ignore # noqa: F821
