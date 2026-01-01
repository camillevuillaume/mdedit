# pylint: disable=redefined-outer-name
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
""" File operations tests for mdedit application. """

# import os
# import sys
# import threading
# import time
from pathlib import Path

import pytest
import webview

from mdedit import app

# import webview


# Get project root (parent of test directory)
project_root = Path(__file__).parent.parent
dist_folder = project_root / "src" / "mdedit" / "dist"
tmp_folder = project_root / "tmp"


@pytest.fixture
def temp_md_file():
    """Create a temporary markdown file for testing."""
    with open(tmp_folder / "test_open.md", "w", encoding="utf-8") as md_file:
        content = "# Test Markdown\n\nThis is a test file for mdedit."
        md_file.write(content)


@pytest.fixture
def api_instance():
    """Create an instance of the webview window for testing."""
    api = app.MarkdownAPI()
    return api


def test_open_file(api_instance, temp_md_file):
    """Test opening a markdown file."""
    _ = temp_md_file  # Ensure the temp file is created

    api_instance.filename = "test_open.md"
    api_instance.filedir = str(tmp_folder)
    result = api_instance.open_file()

    assert result["success"] is True
    assert result["content"] is not None
    assert result["content"] == "# Test Markdown\n\nThis is a test file for mdedit."  # noqa: E501


def test_save_file(api_instance):
    """Test saving a markdown file as a new file."""
    content = "# New Markdown\n\nThis is a new test file."
    api_instance.filename = "test_save.md"
    api_instance.filedir = str(tmp_folder)
    result = api_instance.save_file(content)

    assert result is True
    saved_file_path = tmp_folder / "test_save.md"
    assert saved_file_path.exists()
    with open(saved_file_path, "r", encoding="utf-8") as f:
        saved_content = f.read()
        assert saved_content == content


def test_save_file_dialog(api_instance, monkeypatch):
    """Test the save file dialog functionality."""

    # Create a mock window object
    class MockWindow:
        def create_file_dialog(self, *_args, **_kwargs):
            return (str(tmp_folder / "test_dialog_save.md"),)

    # Mock the webview.windows list with our mock window
    monkeypatch.setattr(webview, "windows", [MockWindow()])

    result = api_instance.save_file_dialog()

    assert result is True
    assert api_instance.filename == "test_dialog_save.md"
    assert api_instance.filedir == str(tmp_folder)


def test_save_file_dialog_cancel(api_instance, monkeypatch):
    """Test the save file dialog functionality."""
    api_instance.filename = "cancel.md"
    api_instance.filedir = "cancel_dir"

    # Create a mock window object
    class MockWindow:
        def create_file_dialog(self, *_args, **_kwargs):
            return None

    # Mock the webview.windows list with our mock window
    monkeypatch.setattr(webview, "windows", [MockWindow()])

    result = api_instance.save_file_dialog()

    assert result is False
    assert api_instance.filename == "cancel.md"
    assert api_instance.filedir == "cancel_dir"
