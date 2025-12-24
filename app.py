import os
from pathlib import Path

import webview


class MarkdownAPI:
    """
    Python code to handle operations from the frontend
    """

    def save_file(self, content, filename="document.md"):
        """Save markdown content to file"""
        try:
            # Ensure .md extension
            if not filename.endswith(".md"):
                filename += ".md"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            return {"success": True, "message": f"Saved to {filename}"}
        except (OSError, IOError) as e:
            return {"success": False, "message": f"File operation failed: {str(e)}"}

    def save_file_dialog(self, content):
        """Open save dialog and save file"""
        try:
            result = webview.windows[0].create_file_dialog(
                webview.FileDialog.SAVE,
                directory=str(Path.home()),
                save_filename="document.md",
                file_types=("Markdown Files (*.md)",),
            )
            if result:
                # create_file_dialog returns a tuple, get first element
                filepath = result[0] if isinstance(result, tuple) else result
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                return {"success": True, "message": f"Saved to {filepath}"}
            return {"success": False, "message": "Save cancelled"}
        except (OSError, IOError) as e:
            return {"success": False, "message": f"File operation failed: {str(e)}"}

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
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                return {
                    "success": True,
                    "content": content,
                    "filepath": filepath,
                    "filename": Path(filepath).name,
                    "message": f"Opened {filepath}",
                }
            return {"success": False, "message": "Open cancelled"}
        except (OSError, IOError) as e:
            return {"success": False, "message": f"Failed to open file: {str(e)}"}


if __name__ == "__main__":
    api = MarkdownAPI()
    dist_path = os.path.join(os.path.dirname(__file__), "dist", "index.html")
    window = webview.create_window(
        "Markdown Editor", dist_path, js_api=api, width=1200, height=800
    )
    webview.start()
