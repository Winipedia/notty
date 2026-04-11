"""module."""

from pyrig.core.subprocesses import run_subprocess

from notty.rig.cli.shared_subcommands import version


def test_version() -> None:
    """Test function."""
    # invoke the version command and check the output
    res = run_subprocess(["uv", "run", "notty", version.__name__], check=True)
    assert "Is overriding pyrigs default version command" in res.stdout
