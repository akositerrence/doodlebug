from setuptools import setup

setup(
    name = "doodlebug",
    version = "0.1",
    packages = "doodlebug",
    entry_points = {
        "console_scripts": [
            "doodlebug = doodlebug.main:run",
        ],
    }
)