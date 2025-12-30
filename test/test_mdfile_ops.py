import os
import sys
import threading
import time
from pathlib import Path

import pytest
import webview

import mdedit.app as app

# Get project root (parent of test directory)
project_root = Path(__file__).parent.parent
dist_folder = project_root / "src" / "mdedit" / "dist"
tmp_folder = project_root / "tmp"


@pytest.fixture
def temp_md_file():
    """Create a temporary markdown file for testing."""
    with open(tmp_folder / "test.md", "w", encoding="utf-8") as md_file:
        content = "# Test Markdown\n\nThis is a test file for mdedit."
        md_file.write(content)


@pytest.fixture
def api_instance():
    """Create an instance of the webview window for testing."""
    api = app.MarkdownAPI()
    return api


def test_open_file(temp_md_file, api_instance):
    """Test opening a markdown file."""
    api_instance.filename = "test.md"
    api_instance.filedir = str(tmp_folder)
    result = api_instance.open_file()

    assert result["success"] is True
    assert result["content"] is not None
    assert result["content"] == "# Test Markdown\n\nThis is a test file for mdedit."
