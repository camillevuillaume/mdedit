# pylint: disable=redefined-outer-name
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
"""File operations tests for mdedit application."""

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
    """Test opening a markdown file and verifying its content.

    This test verifies that:
    - A markdown file can be successfully opened
    - The method returns True on successful open
    - The content matches the expected test content
    """
    _ = temp_md_file  # Ensure the temp file is created

    api_instance.filename = "test_open.md"
    api_instance.filedir = str(tmp_folder)
    result = api_instance.open_file()

    assert result["success"] is True
    assert result["content"] is not None
    assert result["content"] == "# Test Markdown\n\nThis is a test file for mdedit."  # noqa: E501


def test_save_file(api_instance):
    """Test saving a markdown file as a new file.

    This test verifies that:
    - A markdown file can be successfully saved to disk
    - The method returns True on successful save
    - The saved file exists and contains the expected content
    """
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


def test_save_file_dialog(api_instance):
    """Test the save file dialog functionality when saving a file.

    A save file dialog is mocked, and returns a valid file path.
    This test verifies that:
    - The filename and filedir attributes are properly set on the API instance
    - The method returns True on successful operation
    """

    # Create a mock window object that simulates a successful file dialog
    class MockWindow:
        def create_file_dialog(self, *_args, **_kwargs):
            return (str(tmp_folder / "test_dialog_save.md"),)

    # Set up the window on the API instance
    mock_window = MockWindow()
    api_instance.window = mock_window

    result = api_instance.save_file_dialog()

    assert result is True
    assert api_instance.filename == "test_dialog_save.md"
    assert api_instance.filedir == str(tmp_folder)


def test_save_file_dialog_cancel(api_instance):
    """Test the save file dialog functionality when user cancels the dialog.

    A save file dialog is mocked and returns None to simulate cancel.
    This test verifies that:
    - The method returns False when dialog is cancelled
    - The filename and filedir attributes remain unchanged when cancelled
    """
    # Set up initial values
    api_instance.filename = "cancel.md"
    api_instance.filedir = "cancel_dir"

    # Create a mock window object that simulates a cancelled file dialog
    class MockWindow:
        def create_file_dialog(self, *_args, **_kwargs):
            return None

    # Set up the window on the API instance
    mock_window = MockWindow()
    api_instance.window = mock_window

    result = api_instance.save_file_dialog()

    assert result is False
    assert api_instance.filename == "cancel.md"
    assert api_instance.filedir == "cancel_dir"


# Additional comprehensive tests added for better test coverage
def test_mark_modified(api_instance):
    """Test marking document as modified and verifying the modified status.

    This test verifies that:
    - The document starts with modified status set to False
    - Calling mark_modified() correctly sets the modified status to True
    - The is_modified() property accurately reflects the modification status
    """
    assert api_instance.is_modified() is False
    api_instance.mark_modified()
    assert api_instance.is_modified() is True


def test_open_file_with_nonexistent_file(api_instance):
    """Test opening a file that doesn't exist and verifying error handling.

    This test verifies that:
    - Attempting to open a non-existent file returns success=False
    - The content returned is an empty string
    - Proper error handling is implemented for missing files
    """
    api_instance.filename = "nonexistent.md"
    api_instance.filedir = "/tmp"

    result = api_instance.open_file()

    assert result["success"] is False
    assert result["content"] == ""


def test_is_modified_property(api_instance):
    """Test that is_modified property accurately reflects document modification status.

    This test verifies that:
    - The is_modified property correctly returns False for unmodified documents
    - The is_modified property correctly returns True after mark_modified() is called
    - The property accurately reflects the current modification state
    """
    assert api_instance.is_modified() is False
    api_instance.mark_modified()
    assert api_instance.is_modified() is True


def test_save_file_with_empty_content(api_instance):
    """Test saving file with empty content and verifying no crashes.

    This test verifies that:
    - The save_file method can handle empty content without crashing
    - The method returns True for successful empty content save
    - No exceptions are raised during the operation
    """
    # Set up a valid file path
    api_instance.filename = "test_empty.md"
    api_instance.filedir = str(tmp_folder)

    result = api_instance.save_file("")

    # This should not crash
    assert result is True  # The method should not crash
