import os
import re
from setuptools import setup


def get_version():
    """Return the package version as listed in `__version__` in `__init.py__`."""
    with open(os.path.join("demerzel", "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """Return the contents in `README.md`."""
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="demerzel",
    version=get_version(),
    author="Wayde Gilliam",
    author_email="waydegilliam@gmail.com",
    url="https://github.com/waydegg/demerzel",
    description="Simple workflow scheduling and monitoring",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    python_requires=">=3.9",
    packages=["demerzel"],
    install_requires=[
        "uvloop>=0.16.0",
        "croniter>=1.0.13",
        "pytz>=2021.1"
    ],
    extras_require={
        "quality": [
            "black==21.9b0",
            "mypy==0.910",
            "autoflake==1.4",
            "isort==5.9.3",
            "flake8==3.9.2"
        ],
        "build": [
            "twine==3.4.2",
            "wheel==0.37.0"
        ]
    }
)
