"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from typing import TYPE_CHECKING, Any, cast

from pyrig.rig.configs.base.workflow import (  # deptry: ignore[DEP004]
    WorkflowConfigFile as BaseWorkflowConfigFile,
)
from pyrig.rig.configs.pyproject import (  # deptry: ignore[DEP004]
    PyprojectConfigFile as BasePyprojectConfigFile,
)
from pyrig_codecov.rig.configs.version_control.remote.workflows.health_check import (  # deptry: ignore[DEP004]  # noqa: E501
    HealthCheckWorkflowConfigFile as BaseHealthCheckWorkflowConfigFile,
)
from pyrig_executables.rig.configs.version_control.remote.workflows.release import (  # deptry: ignore[DEP004]  # noqa: E501
    ReleaseWorkflowConfigFile as BaseReleaseWorkflowConfigFile,
)

from notty.rig.tools.type_checker import TypeChecker

if TYPE_CHECKING:
    from types import MethodType


class WorkflowConfigFileMixin(BaseWorkflowConfigFile):
    """Mixin to add PySide6-specific workflow steps.

    This mixin provides common overrides for PySide6 workflows to work on
    GitHub Actions headless Linux environments.
    """

    def steps_core_installed_setup(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Get the setup steps.

        We need to install additional system dependencies for pyside6.
        """
        steps = super().steps_core_installed_setup(
            *args,
            **kwargs,
        )

        index = next(
            i
            for i, step in enumerate(steps)
            if step["id"]
            == self.id_from_method(cast("MethodType", self.step_install_dependencies))
        )
        steps.insert(index + 1, self.step_pre_install_pygame_from_binary())
        return steps

    def step_pre_install_pygame_from_binary(self) -> dict[str, Any]:
        """Get the step to install PySide6 dependencies."""
        return self.step(
            cast("MethodType", self.step_pre_install_pygame_from_binary),
            run="uv pip install pygame --only-binary=:all:",
        )


class HealthCheckWorkflowConfigFile(
    WorkflowConfigFileMixin, BaseHealthCheckWorkflowConfigFile
):
    """Health check workflow.

    Extends winipedia_utils health check workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class ReleaseWorkflowConfigFile(WorkflowConfigFileMixin, BaseReleaseWorkflowConfigFile):
    """Release workflow.

    Extends winipedia_utils release workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class PyprojectConfigFile(BasePyprojectConfigFile):
    """Pyproject config file.

    Extends winipedia_utils pyproject config file to add additional config.
    """

    def _configs(self) -> dict[str, Any]:
        """Get the configs."""
        configs = super()._configs()

        # add mypy settings
        configs["tool"][TypeChecker.I.name()] = {  # type: ignore[call-arg]
            "strict": True,
            "warn_unreachable": True,
            "show_error_codes": True,
            "files": ".",
        }
        return configs
