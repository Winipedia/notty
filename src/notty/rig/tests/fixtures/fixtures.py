"""Defines pytest fixtures."""

import pytest
from pyrig.rig.tests.fixtures.autouse.session import (
    package_manager_updated as pyrig_package_manager_updated,
)

override_works = False


@pytest.fixture(scope="session")
def package_manager_updated() -> None:
    """Overrides pyrigs fixture of the same name to check overriding works correctly."""
    global override_works  # noqa: PLW0603
    override_works = True
    assert override_works, "Fixture override did not work as expected"


@pytest.fixture(scope="session", autouse=True)
def assert_override_works(package_manager_updated: None) -> None:
    """Checks that the previous fixture override worked as expected."""
    assert pyrig_package_manager_updated.__name__ == "package_manager_updated"
    assert package_manager_updated is None, (
        "Previous fixture override did not run as expected"
    )
    assert override_works, "Previous fixture override did not work as expected"
