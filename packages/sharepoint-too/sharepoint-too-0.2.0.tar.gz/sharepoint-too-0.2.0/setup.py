#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup


def get_version(*file_paths):
    """Retrieves the version from sharepoint_too/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )  # noqa
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("sharepoint_too", "__init__.py")

readme = open("README.md").read()
history = open("HISTORY.md").read()
requirements = open("requirements.txt").readlines()

setup(
    name="sharepoint-too",
    version=version,
    description="""This module will handle authentication for your SharePoint Online/O365 site, allowing you to make straightforward HTTP requests from Python. It extends the commonly used Requests module, meaning that returned objects are familliar, easy to work with and well documented.""",  # noqa
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Tim Santor",
    author_email="tsantor@xstudios.com",
    url="https://github.com/tsantor/sharepoint-too",
    packages=[
        "sharepoint_too",
    ],
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords="sharepoint-too",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
