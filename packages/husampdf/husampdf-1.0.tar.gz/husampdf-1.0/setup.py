from os import path
import setuptools
from setuptools import version
from pathlib import Path

setuptools.setup(
    name = "husampdf",
    version = 1.0,
    long_desc= Path("README.md").read_text(),
     packeges=setuptools.find_packages(exclude=["tests","data"])
)