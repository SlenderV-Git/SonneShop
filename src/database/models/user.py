from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base.core import Base
from src.database.models.mixins import ModelWithTimeMixin, ModelWithIDMixin


class UserModel(ModelWithIDMixin, ModelWithTimeMixin, Base):
    __tablename__ = "user"

    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)

    accounts: Mapped[list["AccountModel"]] = relationship(back_populates="user")  # type: ignore # noqa: F821
    transactions: Mapped[list["TransactionModel"]] = relationship(back_populates="user")  # type: ignore  # noqa: F821
