from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base.core import Base
from src.database.models.mixins import ModelWithTimeMixin, ModelWithIDMixin


class StockLogModel(ModelWithIDMixin, ModelWithTimeMixin, Base):
    __tablename__ = "stock_log"

    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    remaining: Mapped[int] = mapped_column(nullable=False)

    product: Mapped["ProductModel"] = relationship()  # type: ignore  # noqa: F821
