"""Build script.

All subclasses of Builder in the builds package are automatically called.
"""

from types import ModuleType

from pyrig.rig.builders.pyinstaller import PyInstallerBuilder

from notty import main
from notty.rig import resources


class NottyBuilder(PyInstallerBuilder):
    """Builder for notty."""

    def entry_point_module(self) -> ModuleType:
        """Get the entry point module."""
        return main

    def app_icon_png_location(self) -> tuple[str, ModuleType]:
        """Get the app icon PNG location."""
        return "icon", resources
