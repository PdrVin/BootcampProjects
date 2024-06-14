from typing import Annotated
from pydantic import Field
from workout_api.base.schemas import BaseSchema


class CentroTreinamento(BaseSchema):
    nome: Annotated[
        str,
        Field(
            description="Nome da Centro de Treinamento",
            example="CT King",
            max_length=20,
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description="Endereço da Centro de Treinamento",
            example="Rua X, Q2",
            max_length=60,
        ),
    ]
    proprietario: Annotated[
        str,
        Field(
            description="Proprietario da Centro de Treinamento",
            example="Pedro",
            max_length=30,
        ),
    ]
