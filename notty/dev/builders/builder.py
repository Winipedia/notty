"""Build script.

All subclasses of Builder in the builds package are automatically called.
"""

from types import ModuleType

from pyrig.dev.builders.pyinstaller import PyInstallerBuilder


class NottyBuilder(PyInstallerBuilder):
    """Builder for notty."""

    @classmethod
    def get_additional_resource_pkgs(cls) -> list[ModuleType]:
        """Get the add datas."""
        return []
