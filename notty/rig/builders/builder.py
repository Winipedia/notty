"""Build script.

All subclasses of Builder in the builds package are automatically called.
"""

from types import ModuleType

from pyrig.rig.builders.pyinstaller import PyInstallerBuilder


class NottyBuilder(PyInstallerBuilder):
    """Builder for notty."""

    def additional_resource_packages(self) -> list[ModuleType]:
        """Get the add datas."""
        return []
