"""
Tests for the main module.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import main


def test_main_function_exists():
    """Test that the main function exists and is callable."""
    assert callable(main)


def test_main_runs_without_error(capsys):
    """Test that the main function runs without raising an error."""
    main()
    captured = capsys.readouterr()
    assert "Welcome to the Hackathon Project!" in captured.out
