"""Subclassing MirrorTest to test the notty game."""

from pyrig.rig.tests.mirror_test import MirrorTestConfigFile as BaseMirrorTestConfigFile


class MirrorTestConfigFile(BaseMirrorTestConfigFile):
    """Subclassing MirrorTest to test the notty game."""

    def test_func_skeleton(self, test_func_name: str) -> str:
        """Get the test function skeleton."""
        return f'''

def {test_func_name}() -> None:
    """Test function."""
'''

    def test_method_skeleton(self, test_method_name: str) -> str:
        """Get the test method skeleton."""
        return f'''
    def {test_method_name}(self) -> None:
        """Test method."""
'''
