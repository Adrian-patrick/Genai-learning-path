from pydantic import BaseModel, Field


class CriticOutput(BaseModel):
    pass_through: bool
    reason: str
