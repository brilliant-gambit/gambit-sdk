from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gambit_sdk.schemas.unified_solution_schema import UnifiedSolutionExercise


class GambitSDKError(Exception):
    def __init__(
            self,
            message: str,
    ) -> None:
        self.message = message
        super().__init__(self.message)


class SolutionTypeMismatchError(GambitSDKError):
    def __init__(
            self,
            unified_solution_exercise: UnifiedSolutionExercise,
            message: str,
    ) -> None:
        self.unified_solution_exercise = unified_solution_exercise
        super().__init__(message)


class PlatformAuthenticationError(GambitSDKError):
    def __init__(
            self,
            message: str,
    ) -> None:
        super().__init__(message)


class RefreshNotSupportedError(GambitSDKError):
    def __init__(
            self,
            message: str,
    ) -> None:
        super().__init__(message)
