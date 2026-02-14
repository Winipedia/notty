"""Overriding the type checker to get from ty to mypy."""

from pyrig.rig.tools.type_checker import TypeChecker
from pyrig.src.processes import Args


class MypyTypeChecker(TypeChecker):
    """Mypy type checker."""

    def name(self) -> str:
        """Get the name of the type checker."""
        return "mypy"

    def check_args(self, *args: str) -> Args:
        """Get the args for checking types."""
        return self.args(*args)
