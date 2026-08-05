import re
from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent


def get_version():
    """Read version from __init__.py without importing the package.

    Importing deemon at build time pulls in runtime deps (e.g. requests)
    that are not available in pip's isolated build environment.
    """
    init_py = (HERE / "deemon" / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", init_py, re.M)
    if not match:
        raise RuntimeError("Unable to find __version__ in deemon/__init__.py")
    return match.group(1)


with open(HERE / "requirements.txt", encoding="utf-8") as f:
    required = f.read().splitlines()

README = (HERE / "README.md").read_text(encoding="utf-8")
DESCRIPTION = "Monitor new releases by a specified list of artists and auto download using the deemix library"

setup(
    name="deemon",
    version=get_version(),
    author="digitalec",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    license="GPL3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=required,
    url="https://github.com/mon5termatt/deemon",
    entry_points={
        "console_scripts": ["deemon=deemon.__main__:main"],
    },
)
