from datetime import UTC, datetime

from gambit_sdk.schemas import (
    UnifiedAssignmentPreview,
    UnifiedAttempt,
)


def test_assignment_preview_creation() -> None:
    now = datetime.now(UTC)
    preview = UnifiedAssignmentPreview(
        platform_assignment_id="123",
        title="Test Assignment",
        assigned_date=now.date(),
        deadline=now,
        context_data={"custom_field": 1},
    )

    assert preview.title == "Test Assignment"
    assert preview.context_data["custom_field"] == 1

    data = preview.model_dump()
    assert data["platform_assignment_id"] == "123"


def test_attempt_creation_defaults() -> None:
    attempt = UnifiedAttempt(
        platform_attempt_id="att-1",
        platform_assignment_id="asgn-1",
    )
    assert attempt.submission_context == {}
    assert attempt.grade_context == {}
