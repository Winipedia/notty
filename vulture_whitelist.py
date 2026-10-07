"""Explicit references for reviewed dead code false positives."""

from types import MethodType

from pyrig.rig.tools.base.hooks import CheckHookTool
from pyrig.rig.tools.testing.project import ProjectTester

from notty.rig.tools.coverage_tester import CoverageTester
from notty.rig.tools.type_checker import TypeChecker

_TOOLS = (
    CoverageTester,
    TypeChecker,
)
_TOOLS_OVERRIDES = (
    CheckHookTool.check_args,
    ProjectTester.threshold,
)
_TYPE_CHECKING = (MethodType,)
