""" Setup script to build npm assets before packaging the Python project. """
import os
import subprocess

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildNpmCommand(build_py):
    """Custom command to run npm build before packaging."""

    def run(self):
        # 1. Run npm install & build
        # cwd should point to where your package.json is
        frontend_dir = os.path.join(os.path.dirname(__file__), "src", "mdedit", "frontend")

        print("--- Running npm install ---")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)

        print("--- Running npm run build ---")
        subprocess.run(["npm run build"], cwd=frontend_dir, check=True, shell=True)

        # 2. Continue with the standard Python build process
        super().run()


setup(
    cmdclass={
        "build_py": BuildNpmCommand,
    }
)
