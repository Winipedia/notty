"""module."""

from notty.dev.configs.configs import PyprojectConfigFile


class TestNottyGameWorkflowMixin:
    """Test class."""

    def test_steps_core_installed_setup(self) -> None:
        """Test method."""

    def test_step_pre_install_pygame_from_binary(self) -> None:
        """Test method."""


class TestHealthCheckWorkflow:
    """Test class."""


class TestReleaseWorkflow:
    """Test class."""


class TestPyprojectConfigFile:
    """Test class."""

    def test_get_standard_dev_dependencies(self) -> None:
        """Test method."""

    def test_get_dependencies(self) -> None:
        """Test method."""

    def test_get_configs(self) -> None:
        """Test method."""
        configs = PyprojectConfigFile.get_configs()
        assert isinstance(configs, dict)


class TestBuildWorkflow:
    """Test class."""
