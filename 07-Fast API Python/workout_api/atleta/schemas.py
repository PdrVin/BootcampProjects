from workout_api.base.schemas import BaseSchema
from pydantic import Field, PositiveFloat
from typing import Annotated

class Atleta(BaseSchema):
    # Campos
    nome: Annotated[str, Field(description='Nome do Atleta', examples='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do Atleta', examples='12345678901', max_length=11)]
    idade: Annotated[int, Field(description='Idade do Atleta', examples='25')]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta', examples='75.5')]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta', examples='1.80')]
    cpf: Annotated[str, Field(description='Sexo do Atleta', examples='M', max_length=1)]