from typing import Sequence, Tuple, Type

from src.common.dto.base import DTOType
from src.database.models.base import ModelType


def from_model_to_dto(model: ModelType, dto: Type[DTOType]) -> DTOType:
    return dto(**model.as_dict())


def from_list_model_to_list_dto(
    models: Sequence[ModelType], dto: Type[DTOType]
) -> Sequence[DTOType]:
    return [dto(**model.as_dict()) for model in models]


def from_many_models_to_list_dto(
    models: Sequence[Tuple[ModelType]], dto: Type[DTOType]
) -> Sequence[DTOType]:
    dto_list = []
    for models_tuple in models:
        model_dict = {}
        for model in models_tuple:
            model_dict.update(model.as_dict())
        dto_list.append(dto(**model_dict))
    return dto_list
