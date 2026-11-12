"""module."""

from notty.rig.configs.configs import WorkflowConfigFileMixin


class TestBuildWorkflow:
    """Test class."""


class TestBuildWorkflowConfigFile:
    """Test class."""


class TestExecutableWorkflowConfigFile:
    """Test class."""


class TestHealthCheckWorkflow:
    """Test class."""


class TestHealthCheckWorkflowConfigFile:
    """Test class."""


class TestPyprojectConfigFile:
    """Test class."""

    def test__configs(self) -> None:
        """Test method."""


class TestReleaseWorkflow:
    """Test class."""


class TestWorkflowConfigFileMixin:
    """Test class."""

    def test_step_pre_install_pygame_from_binary(self) -> None:
        """Check Pygame is installed from a binary wheel."""
        step = WorkflowConfigFileMixin.I.step_pre_install_pygame_from_binary()
        assert step["run"] == "uv pip install pygame --only-binary=:all:"

    def test_steps_core_installed_setup(self) -> None:
        """Check the Pygame wheel is installed after dependencies."""
        steps = WorkflowConfigFileMixin.I.steps_core_installed_setup()
        ids = [step["id"] for step in steps]
        assert ids[ids.index("install-dependencies") + 1] == (
            "pre-install-pygame-from-binary"
        )
