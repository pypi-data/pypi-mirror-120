"""Tests the bugyi_dummy.cli module."""

from bugyi_dummy.cli import main


def test_main() -> None:
    """Tests main() function."""
    assert main([""]) == 0
