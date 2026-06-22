"""Pytest-cov coverage testing wrapper.

Provides type-safe wrapper for pytest-cov commands for code coverage analysis.
Shows coverage badge from Codecov.io.

Example:
    >>> from pyrig_codecov.rig.tools.coverage_tester import (
    ...     CoverageTester,
    ... )
    >>> CoverageTester.I.remote_coverage_url()
"""

from pyrig_codecov.rig.tools.testers.coverage import (  # deptry: ignore[DEP004]
    CoverageTester as BaseCoverageTester,
)


class CoverageTester(BaseCoverageTester):
    """You can override methods from the base class to customize behavior."""

    def threshold(self) -> int:
        """Override this method to set a custom coverage threshold."""
        return 0
