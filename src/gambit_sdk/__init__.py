"""
Gambit Platform Integration SDK

This package provides all the necessary components for developing a platform adapter
for the Gambit system.

The main entry points are:
- BaseAdapter: The abstract base class that every adapter must implement.
- AssignmentType: An enumeration of all supported assignment types.
- Unified*: A collection of Pydantic models representing the standardized data
  structures used for communication with the Gambit CORE system.
"""

from .base_adapter import BaseAdapter
from .enums import ExerciseType
from .schemas import (
    SingleChoiceAnswer,
    MultipleChoiceAnswer,
    ChoiceStructure,
    MatchingAnswer,
    MatchingStructure,
    OrderingAnswer,
    OrderingStructure,
    StringAnswer,
    TextAnswer,
    TextFileAnswer,
    UnifiedAssignmentDetails,
    UnifiedAssignmentPreview,
    UnifiedAttempt,
    UnifiedExercise,
    UnifiedGrade,
    UnifiedSolution,
    UnifiedSolutionExercise,
)
from . import errors, utils

__all__ = [
    "BaseAdapter",
    "SingleChoiceAnswer",
    "MultipleChoiceAnswer",
    "ChoiceStructure",
    "ExerciseType",
    "MatchingAnswer",
    "MatchingStructure",
    "OrderingAnswer",
    "OrderingStructure",
    "StringAnswer",
    "TextAnswer",
    "TextFileAnswer",
    "UnifiedAssignmentDetails",
    "UnifiedAssignmentPreview",
    "UnifiedAttempt",
    "UnifiedExercise",
    "UnifiedGrade",
    "UnifiedSolution",
    "UnifiedSolutionExercise",
    "errors",
    "utils",
]
