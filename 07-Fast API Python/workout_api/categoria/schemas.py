from typing import Annotated
from pydantic import Field
from workout_api.base.schemas import BaseSchema


class Categoria(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome da Categoria", example="Scale", max_length=10)
    ]
