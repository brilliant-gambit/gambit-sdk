from typing import Any

from pydantic import BaseModel, Field


class UnifiedAuthSession(BaseModel):
    cookies: dict[str, str] = Field(default_factory=dict)
    headers: dict[str, str] = Field(default_factory=dict)
    refresh_data: dict[str, Any] = Field(default_factory=dict)
