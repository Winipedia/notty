"""Overriding the type checker to get from ty to mypy."""

from pyrig.rig.tools.type_checker import TypeChecker
from pyrig.src.processes import Args


class MypyTypeChecker(TypeChecker):
    """Mypy type checker."""

    @classmethod
    def name(cls) -> str:
        """Get the name of the type checker."""
        return "mypy"

    @classmethod
    def check_args(cls, *args: str) -> Args:
        """Get the args for checking types."""
        return cls.args(*args)
