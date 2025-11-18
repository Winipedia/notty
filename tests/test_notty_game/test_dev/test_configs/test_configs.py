"""module."""

from notty_game.dev.configs.configs import NottyGameWorkflowMixin, ReleaseWorkflow


class TestNottyGameWorkflowMixin:
    """Test class for NottyGameWorkflowMixin."""

    def test_steps_core_installed_setup(self) -> None:
        """Test method for steps_core_matrix_setup."""
        # just assert that the method returns a list of dicts
        steps = NottyGameWorkflowMixin.steps_core_installed_setup()
        assert isinstance(steps, list), f"Expected list, got {type(steps)}"
        # assert insall pygame system dependencies is in the list of steps
        assert any(
            step["id"]
            == NottyGameWorkflowMixin.step_pre_install_pygame_from_binary().get("id")
            for step in steps
        ), "Expected install pygame system dependencies step"

    def test_step_pre_install_pygame_from_binary(self) -> None:
        """Test method for step_install_pygame_system_dependencies."""
        # just assert that the method returns a dict
        step = NottyGameWorkflowMixin.step_pre_install_pygame_from_binary()
        assert isinstance(step, dict), f"Expected dict, got {type(step)}"


class TestHealthCheckWorkflow:
    """Test class for HealthCheckWorkflow."""


class TestReleaseWorkflow:
    """Test class for ReleaseWorkflow."""

    def test_steps_release(self) -> None:
        """Test method for steps_release."""
        # just assert that the method returns a list of dicts
        steps = ReleaseWorkflow.steps_release()
        assert isinstance(steps, list), f"Expected list, got {type(steps)}"
        # assert insall pygame system dependencies is in the list of steps
        assert any(
            step["id"]
            == NottyGameWorkflowMixin.step_pre_install_pygame_from_binary().get("id")
            for step in steps
        ), "Expected install pygame system dependencies step"
