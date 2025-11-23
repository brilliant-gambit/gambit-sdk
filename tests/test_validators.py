import pytest
from pydantic import ValidationError

from gambit_sdk.enums import ExerciseType
from gambit_sdk.errors import SolutionTypeMismatchError
from gambit_sdk.schemas import (
    SingleChoiceAnswer,
    StringAnswer,
    UnifiedSolutionExercise,
)


def test_unified_solution_exercise_valid_single_choice() -> None:
    exercise = UnifiedSolutionExercise(
        platform_exercise_id="ex-1",
        exercise_type=ExerciseType.CHOICE_SINGLE,
        answer=SingleChoiceAnswer(selected_id="opt-1"),
    )
    assert exercise.platform_exercise_id == "ex-1"
    assert isinstance(exercise.answer, SingleChoiceAnswer)


def test_unified_solution_exercise_mismatch_type() -> None:
    with pytest.raises(SolutionTypeMismatchError) as exc_info:
        UnifiedSolutionExercise(
            platform_exercise_id="ex-2",
            exercise_type=ExerciseType.CHOICE_SINGLE,
            answer=StringAnswer(value="some text"),
        )

    assert "Type mismatch" in str(exc_info.value)


def test_unified_solution_exercise_unsupported() -> None:
    exercise = UnifiedSolutionExercise(
        platform_exercise_id="ex-3",
        exercise_type=ExerciseType.UNSUPPORTED,
        answer=StringAnswer(value="Whatever"),
    )
    assert exercise.exercise_type == ExerciseType.UNSUPPORTED


def test_pydantic_validation_error_structure() -> None:
    with pytest.raises(ValidationError):
        UnifiedSolutionExercise(
            platform_exercise_id="ex-4",
            exercise_type=ExerciseType.CHOICE_SINGLE,
            answer={"wrong": "dict instead of model"},  # pyright: ignore [reportArgumentType]
        )
