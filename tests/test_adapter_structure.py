from typing import Any

import pytest
from httpx import AsyncClient

from gambit_sdk.base_adapter import BaseAdapter
from gambit_sdk.schemas import (
    UnifiedAssignmentDetails,
    UnifiedAssignmentPreview,
    UnifiedAttempt,
    UnifiedAuthSession,
    UnifiedCredentials,
    UnifiedGrade,
    UnifiedSolution,
)


async def test_cannot_instantiate_abstract_adapter() -> None:
    client = AsyncClient()
    with pytest.raises(TypeError):
        BaseAdapter(session=client)  # pyright: ignore [reportAbstractUsage]
    await client.aclose()


async def test_concrete_adapter_implementation() -> None:
    class ConcreteAdapter(BaseAdapter):
        async def login(self, credentials: UnifiedCredentials) -> UnifiedAuthSession:
            return UnifiedAuthSession()

        async def refresh_session(self, refresh_data: dict[str, Any]) -> UnifiedAuthSession:
            return UnifiedAuthSession()

        async def get_assignment_previews(self) -> list[UnifiedAssignmentPreview]:
            return []

        async def get_assignment_details(
            self,
            assignment: UnifiedAssignmentPreview,
        ) -> tuple[UnifiedAssignmentDetails, UnifiedAttempt]:
            raise NotImplementedError

        async def submit_solution(
            self,
            attempt: UnifiedAttempt,
            solution: UnifiedSolution,
        ) -> UnifiedGrade | None:
            return None

        async def get_grade(
            self,
            attempt: UnifiedAttempt,
        ) -> UnifiedGrade | None:
            return None

    client = AsyncClient()
    adapter = ConcreteAdapter(session=client)

    new_auth_session = UnifiedAuthSession(
        headers={"Authorization": "Bearer 123", "User-Agent": "NewAgent"},
        cookies={"session_id": "abc", "old_cookie": "new_val"},
    )
    adapter.load_session(new_auth_session)

    assert adapter.session.headers["Authorization"] == "Bearer 123"
    assert adapter.session.headers["User-Agent"] == "NewAgent"

    assert adapter.session.cookies["session_id"] == "abc"
    assert adapter.session.cookies["old_cookie"] == "new_val"

    assert adapter.session is client

    res = await adapter.get_assignment_previews()
    assert res == []

    await client.aclose()
