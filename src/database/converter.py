from typing import Sequence, Type

from src.common.dto.base import DTOType
from src.database.models.base import ModelType


def from_model_to_dto(model: ModelType, dto: Type[DTOType]) -> DTOType:
    return dto(**model.as_dict())


def from_list_model_to_list_dto(
    models: Sequence[ModelType], dto: Type[DTOType]
) -> Sequence[DTOType]:
    return [dto(**model.as_dict()) for model in models]
