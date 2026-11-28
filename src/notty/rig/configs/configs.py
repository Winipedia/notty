"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from collections.abc import Callable
from typing import Any, override

from pyrig.rig.configs.base.workflow import (  # deptry: ignore[DEP004]
    WorkflowConfigFile as BaseWorkflowConfigFile,
)
from pyrig.rig.configs.pyproject import (  # deptry: ignore[DEP004]
    PyprojectConfigFile as BasePyprojectConfigFile,
)
from pyrig_codecov.rig.configs.version_control.remote.workflows.health_check import (  # deptry: ignore[DEP004]  # noqa: E501
    HealthCheckWorkflowConfigFile as BaseHealthCheckWorkflowConfigFile,
)
from pyrig_executables.rig.configs.version_control.remote.workflows.executable import (  # deptry: ignore[DEP004]  # noqa: E501
    ExecutableWorkflowConfigFile as BaseExecutableWorkflowConfigFile,
)

from notty.rig.tools.type_checker import TypeChecker


class PyprojectConfigFile(BasePyprojectConfigFile):
    """Pyproject config file.

    Extends winipedia_utils pyproject config file to add additional config.
    """

    @override
    def _configs(self) -> dict[str, Any]:
        """Get the configs."""
        configs = super()._configs()

        # add mypy settings
        configs["tool"][TypeChecker.I.name()] = {
            "strict": True,
            "warn_unreachable": True,
            "enable_error_code": [],
            "show_error_code_links": True,
            "files": ".",
        }
        return configs


class WorkflowConfigFileMixin(BaseWorkflowConfigFile):
    """Install Pygame from a binary wheel in test and executable workflows."""

    @override
    def steps_core_installed_setup(
        self,
        *,
        python_version: str | None = None,
        update_dependencies: bool = False,
    ) -> tuple[Callable[[], dict[str, Any]], ...]:
        """Install the Pygame wheel after project dependencies."""
        steps = list(
            super().steps_core_installed_setup(
                python_version=python_version,
                update_dependencies=update_dependencies,
            ),
        )

        index = steps.index(self.step_install_dependencies) + 1
        steps.insert(index, self.step_pre_install_pygame_from_binary)
        return tuple(steps)

    def step_pre_install_pygame_from_binary(self) -> dict[str, Any]:
        """Install Pygame without building it from source."""
        return self.step(
            run="uv pip install pygame --only-binary=:all:",
        )


class ExecutableWorkflowConfigFile(
    WorkflowConfigFileMixin,
    BaseExecutableWorkflowConfigFile,
):
    """Build executables with the Pygame binary wheel installed."""


class HealthCheckWorkflowConfigFile(
    WorkflowConfigFileMixin,
    BaseHealthCheckWorkflowConfigFile,
):
    """Run health checks with the Pygame binary wheel installed."""
