"""Subclassing MirrorTest to test the notty game."""

from pyrig.rig.tests.mirror_test import MirrorTestConfigFile


class NottyMirrorTestConfigFile(MirrorTestConfigFile):
    """Subclassing MirrorTest to test the notty game."""

    @classmethod
    def get_test_func_skeleton(cls, test_func_name: str) -> str:
        """Get the test function skeleton."""
        return f'''

def {test_func_name}() -> None:
    """Test function."""
'''

    @classmethod
    def get_test_method_skeleton(cls, test_method_name: str) -> str:
        """Get the test method skeleton."""
        return f'''
    def {test_method_name}(self) -> None:
        """Test method."""
'''
