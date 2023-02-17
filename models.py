import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Usuario(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    nome: str = Field(...)
    cpf: str = Field(..., unique=True)
    idade: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "nome": "Joao Paulo",
                "cpf": "000.000.000-00",
                "idade": "18"
            }
        }

class UsuarioUpdate(BaseModel):
    nome: Optional[str]
    cpf: Optional[str]
    idade: Optional[int]

    class Config:
        schema_extra = {
            "examplo": {
                "nome": "Joao Paulo",
                "cpf": "000.000.000-00",
                "idade": "18"
            }
        }