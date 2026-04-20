"""Pytest-cov coverage testing wrapper.

Provides type-safe wrapper for pytest-cov commands for code coverage analysis.
Shows coverage badge from Codecov.io.

Example:
    >>> from pyrig.rig.tools.project_coverage_tester import (
    ...     ProjectCoverageTester,
    ... )
    >>> ProjectCoverageTester.I.remote_coverage_url()
"""

from pyrig.rig.tools.project_coverage_tester import (
    ProjectCoverageTester as BaseProjectCoverageTester,
)


class ProjectCoverageTester(BaseProjectCoverageTester):
    """You can override methods from the base class to customize behavior."""

    def coverage_threshold(self) -> int:
        """Override this method to set a custom coverage threshold."""
        return 0
