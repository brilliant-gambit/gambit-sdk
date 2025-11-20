from typing import Any

from pydantic import BaseModel, Field


class UnifiedAttempt(BaseModel):
    platform_attempt_id: str | None
    platform_assignment_id: str
    submission_context: dict[str, Any] = Field(default_factory=dict)
    grade_context: dict[str, Any] = Field(default_factory=dict)
