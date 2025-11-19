"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from typing import Any

from pyrig.dev.configs.workflows.base.base import (
    Workflow as WinipediaWorkflow,
)
from pyrig.dev.configs.workflows.health_check import (
    HealthCheckWorkflow as WinipediaHealthCheckWorkflow,
)
from pyrig.dev.configs.workflows.release import (
    ReleaseWorkflow as WinipediaReleaseWorkflow,
)


class NottyGameWorkflowMixin(WinipediaWorkflow):
    """Mixin to add PySide6-specific workflow steps.

    This mixin provides common overrides for PySide6 workflows to work on
    GitHub Actions headless Linux environments.
    """

    @classmethod
    def steps_core_installed_setup(
        cls, python_version: str | None = None, *, repo_token: bool = False
    ) -> list[dict[str, Any]]:
        """Get the poetry setup steps.

        We need to install additional system dependencies for pyside6.
        """
        steps = super().steps_core_installed_setup(
            python_version, repo_token=repo_token
        )

        index = next(
            i
            for i, step in enumerate(steps)
            if step["id"] == cls.make_id_from_func(cls.step_install_python_dependencies)
        )
        steps.insert(index, cls.step_pre_install_pygame_from_binary())
        return steps

    @classmethod
    def step_pre_install_pygame_from_binary(cls) -> dict[str, Any]:
        """Get the step to install PySide6 dependencies."""
        return cls.get_step(
            step_func=cls.step_pre_install_pygame_from_binary,
            run="pip install pygame --only-binary=:all:",
        )


class HealthCheckWorkflow(NottyGameWorkflowMixin, WinipediaHealthCheckWorkflow):
    """Health check workflow.

    Extends winipedia_utils health check workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class ReleaseWorkflow(HealthCheckWorkflow, WinipediaReleaseWorkflow):
    """Release workflow.

    Extends winipedia_utils release workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """
