"""
A simple markdown editor using pywebview
"""

import logging
import os
from pathlib import Path

import webview


class MarkdownAPI:
    """
    Python code to handle operations from the frontend
    """

    filename = ""
    filedir = ""
    modified = False

    def mark_modified(self):
        """Mark document as modified"""
        self.modified = True

    def save_file_as(self, content):
        """Save markdown content to a new file"""
        self.filename = ""
        self.filedir = ""
        return self.save_file(content)

    def save_file(self, content):
        """Save markdown content to file"""
        if not self.filename or not self.filedir:
            # Open save dialog if filename or path not defined
            if not self.save_file_dialog():
                logging.info("File operation failed")
                return False
        # Save content to file
        try:
            filepath = os.path.join(self.filedir, self.filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logging.info("Saved to %s", self.filename)
            self.modified = False
            return True
        except (OSError, IOError) as e:
            logging.error("File operation failed: %s", str(e))
            return False

    def save_file_dialog(self):
        """Open save dialog and save file
        in case file name and path not yet defined"""
        try:
            if self.filedir:
                initial_dir = self.filedir
            else:
                initial_dir = str(Path.home())
            result = webview.windows[0].create_file_dialog(
                webview.FileDialog.SAVE,
                directory=initial_dir,
                save_filename="document.md",
                file_types=("Markdown Files (*.md)",),
            )
            if result:
                # create_file_dialog returns a tuple, get first element
                filepath = result[0] if isinstance(result, tuple) else result
                self.filedir, self.filename = os.path.split(filepath)
                if not self.filename.endswith(".md"):
                    self.filename += ".md"
                return True
            return False
        except OSError as e:
            logging.error("Error trying to save file: %s", str(e))
            return False

    def open_file_dialog(self):
        """Open file dialog and load markdown file"""
        try:
            result = webview.windows[0].create_file_dialog(
                webview.FileDialog.OPEN,
                directory=str(Path.home()),
                allow_multiple=False,
                file_types=("Markdown Files (*.md)", "All Files (*.*)"),
            )
            if result:
                # create_file_dialog returns a tuple, get first element
                filepath = result[0] if isinstance(result, tuple) else result
                self.filedir, self.filename = os.path.split(filepath)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                logging.info("Opened %s", filepath)
                self.modified = False
                return {"success": True, "content": content}
            logging.info("Open cancelled")
            return {"success": False, "content": ""}
        except (OSError, IOError) as e:
            logging.error("Failed to open file: %s", str(e))
            return {"success": False, "content": ""}


if __name__ == "__main__":
    api = MarkdownAPI()
    dist_path = os.path.join(os.path.dirname(__file__), "dist", "index.html")
    window = webview.create_window(
        "Markdown Editor", dist_path, js_api=api, width=1200, height=800
    )
    webview.start()
