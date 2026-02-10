"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

import re
from typing import Any

from pyrig.rig.configs.base.workflow import (
    Workflow as PyrigWorkflow,
)
from pyrig.rig.configs.pyproject import (
    PyprojectConfigFile as PyrigPyprojectConfigFile,
)
from pyrig.rig.configs.workflows.build import (
    BuildWorkflow as PyrigBuildWorkflow,
)
from pyrig.rig.configs.workflows.health_check import (
    HealthCheckWorkflow as PyrigHealthCheckWorkflow,
)
from pyrig.rig.configs.workflows.release import (
    ReleaseWorkflow as PyrigReleaseWorkflow,
)


class NottyGameWorkflowMixin(PyrigWorkflow):
    """Mixin to add PySide6-specific workflow steps.

    This mixin provides common overrides for PySide6 workflows to work on
    GitHub Actions headless Linux environments.
    """

    @classmethod
    def steps_core_installed_setup(
        cls,
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
            if step["id"] == cls.make_id_from_func(cls.step_install_dependencies)
        )
        steps.insert(index + 1, cls.step_pre_install_pygame_from_binary())
        return steps

    @classmethod
    def step_pre_install_pygame_from_binary(cls) -> dict[str, Any]:
        """Get the step to install PySide6 dependencies."""
        return cls.get_step(
            step_func=cls.step_pre_install_pygame_from_binary,
            run="uv pip install pygame --only-binary=:all:",
        )


class HealthCheckWorkflow(NottyGameWorkflowMixin, PyrigHealthCheckWorkflow):
    """Health check workflow.

    Extends winipedia_utils health check workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class ReleaseWorkflow(NottyGameWorkflowMixin, PyrigReleaseWorkflow):
    """Release workflow.

    Extends winipedia_utils release workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class BuildWorkflow(NottyGameWorkflowMixin, PyrigBuildWorkflow):
    """Build workflow.

    Extends winipedia_utils build workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class PyprojectConfigFile(PyrigPyprojectConfigFile):
    """Pyproject config file.

    Extends winipedia_utils pyproject config file to add additional config.
    """

    @classmethod
    def _get_configs(cls) -> dict[str, Any]:
        """Get the configs."""
        configs = super()._get_configs()

        # not testing, so adjust pytest addopts
        addopts = configs["tool"]["pytest"]["ini_options"]["addopts"]
        # use regex to replace --cov-fail-under=SOME_NUMBER with --cov-fail-under=0
        configs["tool"]["pytest"]["ini_options"]["addopts"] = re.sub(
            r"--cov-fail-under=\d+", "--cov-fail-under=0", addopts
        )

        # add mypy settings
        configs["tool"]["mypy"] = {
            "strict": True,
            "warn_unreachable": True,
            "show_error_codes": True,
            "files": ".",
        }
        return configs

    @classmethod
    def get_dependencies(cls) -> list[str]:
        """Get the dependencies."""
        deps = super().get_dependencies()
        # add pygame
        return sorted([*["pygame", "platformdirs"], *deps])
