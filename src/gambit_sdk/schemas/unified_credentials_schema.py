from typing import Any

from pydantic import BaseModel, Field


class UnifiedCredentials(BaseModel):
    username: str
    password: str
    extra_params: dict[str, Any] = Field(default_factory=dict)
