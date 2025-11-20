from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field

from gambit_sdk.schemas.unified_exercise_schema import UnifiedExercise


class UnifiedAssignmentPreview(BaseModel):
    platform_assignment_id: str
    title: str
    assigned_date: date
    deadline: datetime
    context_data: dict[str, Any] = Field(default_factory=dict)


class UnifiedAssignmentDetails(UnifiedAssignmentPreview):
    description: str | None = None
    exercises: list[UnifiedExercise]
