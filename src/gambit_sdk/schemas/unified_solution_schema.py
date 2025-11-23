from __future__ import annotations

from pydantic import BaseModel, model_validator

from gambit_sdk.enums.exercise_type_enum import ExerciseType
from gambit_sdk.errors.gambit_sdk_errors import SolutionTypeMismatchError
from gambit_sdk.schemas.solution_type_schemas import (
    MatchingAnswer,
    MultipleChoiceAnswer,
    OrderingAnswer,
    SingleChoiceAnswer,
    StringAnswer,
    TextAnswer,
    TextFileAnswer,
)


class UnifiedSolutionExercise(BaseModel):
    platform_exercise_id: str
    exercise_type: ExerciseType
    answer: (
        SingleChoiceAnswer
        | MultipleChoiceAnswer
        | StringAnswer
        | TextAnswer
        | TextFileAnswer
        | MatchingAnswer
        | OrderingAnswer
    )

    @model_validator(mode="after")
    def check_exercise_type_match(self) -> UnifiedSolutionExercise:
        from gambit_sdk.utils.exercise_type_to_answer_class import EXERCISE_TYPE_TO_ANSWER_CLASS  # noqa: PLC0415

        if self.exercise_type == ExerciseType.UNSUPPORTED:
            return self

        expected_class = EXERCISE_TYPE_TO_ANSWER_CLASS.get(self.exercise_type)

        if expected_class is None:
            raise SolutionTypeMismatchError(
                unified_solution_exercise=self,
                message=f"Unknown or unmapped exercise type: {self.exercise_type}",
            )

        if not isinstance(self.answer, expected_class):
            raise SolutionTypeMismatchError(
                unified_solution_exercise=self,
                message=(
                    f"Type mismatch! "
                    f"Exercise type is '{self.exercise_type.value}', which requires '{expected_class.__name__}', "
                    f"but got '{type(self.answer).__name__}'."
                ),
            )

        return self


class UnifiedSolution(BaseModel):
    platform_assignment_id: str
    answers: list[UnifiedSolutionExercise]
