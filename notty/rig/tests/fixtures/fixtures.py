"""Defines pytest fixtures."""

import pytest

override_works = False


@pytest.fixture(scope="session")
def assert_project_mgt_is_up_to_date() -> None:
    """Overrides pyrigs fixture of the same name to check overriding works correctly."""
    global override_works  # noqa: PLW0603
    override_works = True
    assert override_works, "Fixture override did not work as expected"


@pytest.fixture(scope="session", autouse=True)
def assert_override_works(assert_project_mgt_is_up_to_date: None) -> None:
    """Checks that the previous fixture override worked as expected."""
    assert assert_project_mgt_is_up_to_date is None, (
        "Previous fixture override did not run as expected"
    )
    assert override_works, "Previous fixture override did not work as expected"
