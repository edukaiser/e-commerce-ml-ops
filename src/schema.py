from pydantic import BaseModel, Field


class RecommenderInput(BaseModel):
    """Schema para validação da entrada da API."""

    user_idx: int = Field(..., description="Índice numérico do usuário")
    item_idx: int = Field(..., description="Índice numérico do item")


class Config:
    """Configurações extras do Pydantic."""

    frozen: True
