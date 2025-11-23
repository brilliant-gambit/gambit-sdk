import pytest
from httpx import AsyncClient

from gambit_sdk.base_adapter import BaseAdapter
from gambit_sdk.schemas import (
    UnifiedAssignmentDetails,
    UnifiedAssignmentPreview,
    UnifiedAttempt,
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
        async def login(self, username: str, password: str) -> None:
            pass

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

    assert adapter.session is client

    res = await adapter.get_assignment_previews()
    assert res == []

    await client.aclose()
