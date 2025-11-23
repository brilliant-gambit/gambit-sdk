from abc import ABC, abstractmethod

from httpx import AsyncClient

from gambit_sdk.schemas import (
    UnifiedAssignmentDetails,
    UnifiedAssignmentPreview,
    UnifiedAttempt,
    UnifiedGrade,
    UnifiedSolution,
)


class BaseAdapter(ABC):
    def __init__(
            self,
            session: AsyncClient,
    ) -> None:
        self.session = session

    @abstractmethod
    async def login(  # pragma: no cover
            self,
            username: str,
            password: str,
    ) -> None:
        pass

    @abstractmethod
    async def get_assignment_previews(  # pragma: no cover
            self,
    ) -> list[UnifiedAssignmentPreview]:
        pass

    @abstractmethod
    async def get_assignment_details(  # pragma: no cover
            self,
            assignment: UnifiedAssignmentPreview,
    ) -> tuple[UnifiedAssignmentDetails, UnifiedAttempt]:
        pass

    @abstractmethod
    async def submit_solution(  # pragma: no cover
            self,
            attempt: UnifiedAttempt,
            solution: UnifiedSolution,
    ) -> UnifiedGrade | None:
        pass

    @abstractmethod
    async def get_grade(  # pragma: no cover
            self,
            attempt: UnifiedAttempt,
    ) -> UnifiedGrade | None:
        pass
