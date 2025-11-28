from typing import Any

from pydantic import BaseModel, Field, SecretStr


class UnifiedCredentials(BaseModel):
    username: str
    password: SecretStr
    extra_params: dict[str, Any] = Field(default_factory=dict)
