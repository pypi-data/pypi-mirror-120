"""Tests the bugyi.release_tools.cli module."""

from bugyi.release_tools.cli import main


def test_main() -> None:
    """Tests main() function."""
    assert main([""]) == 0
