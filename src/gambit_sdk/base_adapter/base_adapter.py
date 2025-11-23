from abc import ABC, abstractmethod
from typing import Any

from httpx import AsyncClient

from gambit_sdk.schemas import (
    UnifiedAssignmentDetails,
    UnifiedAssignmentPreview,
    UnifiedAttempt,
    UnifiedAuthSession,
    UnifiedCredentials,
    UnifiedGrade,
    UnifiedSolution,
)


class BaseAdapter(ABC):
    def __init__(
            self,
            session: AsyncClient,
    ) -> None:
        self.session = session
        self.refresh_data: dict[str, Any] = {}

    def load_session(self, auth_session: UnifiedAuthSession) -> None:
        if auth_session.cookies:
            self.session.cookies.update(auth_session.cookies)
        if auth_session.headers:
            self.session.headers.update(auth_session.headers)
        self.refresh_data = auth_session.refresh_data

    @abstractmethod
    async def login(  # pragma: no cover
            self,
            credentials: UnifiedCredentials,
    ) -> UnifiedAuthSession:
        pass

    @abstractmethod
    async def refresh_session(  # pragma: no cover
            self,
    ) -> UnifiedAuthSession:
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
