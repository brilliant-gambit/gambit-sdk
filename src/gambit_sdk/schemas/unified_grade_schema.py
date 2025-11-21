from pydantic import BaseModel

from gambit_sdk.schemas.unified_solution_schema import UnifiedSolution


class UnifiedGrade(BaseModel):
    platform_assignment_id: str
    score: float
    max_score: float
    is_passed: bool
    feedback: str | None = None
    correct_solution: UnifiedSolution | None = None
