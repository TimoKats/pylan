"""Python setup.py for agropy package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="agropy",
    version=read("agropy", "version"),
    description="Python library for agricultural management and analysis.",
    url="https://github.com/TimoKats/agropy",
    long_description=read("readme.md"),
    long_description_content_type="text/markdown",
    author="Timo Kats",
    packages=find_packages(exclude=[".github"]),
    install_requires=read_requirements("requirements.txt")
)