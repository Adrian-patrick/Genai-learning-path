from pydantic import BaseModel, Field


class CriticOutput(BaseModel):
    # CHANGED: Added descriptions and defaults for clarity
    pass_through: bool = Field(
        description="Whether the executor response is acceptable"
    )
    reason: str = Field(description="Explanation of the pass_through decision")
