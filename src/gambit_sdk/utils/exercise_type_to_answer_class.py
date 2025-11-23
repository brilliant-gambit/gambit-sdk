from pydantic import BaseModel

from gambit_sdk.enums import ExerciseType
from gambit_sdk.schemas.solution_type_schemas import (
    MatchingAnswer,
    MultipleChoiceAnswer,
    OrderingAnswer,
    SingleChoiceAnswer,
    StringAnswer,
    TextAnswer,
    TextFileAnswer,
)

EXERCISE_TYPE_TO_ANSWER_CLASS: dict[
    ExerciseType,
    type[BaseModel],
] = {
    ExerciseType.CHOICE_SINGLE: SingleChoiceAnswer,
    ExerciseType.CHOICE_MULTIPLE: MultipleChoiceAnswer,
    ExerciseType.INPUT_STRING: StringAnswer,
    ExerciseType.INPUT_TEXT: TextAnswer,
    ExerciseType.TEXT_FILE: TextFileAnswer,
    ExerciseType.MATCHING_PAIRS: MatchingAnswer,
    ExerciseType.SEQUENCE_ORDERING: OrderingAnswer,
}
