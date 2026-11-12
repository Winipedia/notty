"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from typing import TYPE_CHECKING, Any, cast, override

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

if TYPE_CHECKING:
    from types import MethodType


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
        *args: Any,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Install the Pygame wheel after project dependencies."""
        steps = super().steps_core_installed_setup(
            *args,
            **kwargs,
        )

        index = next(
            i
            for i, step in enumerate(steps)
            if step["id"]
            == self.step_id_from_method(
                cast("MethodType", self.step_install_dependencies),
            )
        )
        steps.insert(index + 1, self.step_pre_install_pygame_from_binary())
        return steps

    def step_pre_install_pygame_from_binary(self) -> dict[str, Any]:
        """Install Pygame without building it from source."""
        return self.step(
            cast("MethodType", self.step_pre_install_pygame_from_binary),
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
