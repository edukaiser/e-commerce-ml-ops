from pydantic import BaseModel, Field, field_validator, ConfigDict


class RecommenderInput(BaseModel):
    """Schema para validação da entrada da API."""

    model_config = ConfigDict(frozen=True)

    user_idx: int = Field(..., gt=0, description="Índice positivo do usuário.")
    item_idx: int = Field(..., gt=0, description="Índice positivo do item.")

    @field_validator("user_idx", "item_idx")
    @classmethod
    def must_be_valid_index(cls, v: int) -> int:
        """Valida se o índice é negativo."""
        if v < 0:
            raise ValueError("O índice não pode ser negativo")
        return v
