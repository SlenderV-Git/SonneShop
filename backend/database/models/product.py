from sqlalchemy.orm import Mapped, mapped_column

from backend.database.models.base.core import Base
from backend.database.models.mixins import ModelWithTimeMixin, ModelWithIDMixin


class ProductModel(ModelWithIDMixin, ModelWithTimeMixin, Base):
    __tablename__ = 'product'

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False, unique=True)
    price: Mapped[int] = mapped_column(nullable=False)