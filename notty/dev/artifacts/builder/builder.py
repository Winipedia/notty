"""Build script.

All subclasses of Builder in the builds package are automatically called.
"""

from pathlib import Path

from pyrig.dev.artifacts.builder.base.base import PyInstallerBuilder


class NottyBuilder(PyInstallerBuilder):
    """Builder for notty."""

    @classmethod
    def get_add_datas(cls) -> list[tuple[Path, Path]]:
        """Get the add datas."""
        return []
