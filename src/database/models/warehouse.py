from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base.core import Base
from src.database.models.mixins import ModelWithTimeMixin


class WarehouseModel(ModelWithTimeMixin, Base):
    __tablename__ = "warehouse"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"), unique=True, primary_key=True
    )
    remaining: Mapped[int] = mapped_column(nullable=False)

    product: Mapped["ProductModel"] = relationship()  # type: ignore  # noqa: F821
