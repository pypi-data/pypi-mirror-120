"""
"""

import os
import sys
import setuptools


version_file = "VERSION"
if os.path.exists(version_file):
 with open(version_file, "r") as file:
  __version__ = file.read().strip()
else:
 __version__ = "2021.8"


readme_file = "README.md"
with open("README.md", "r") as file:
 long_description = file.read()


setuptools.setup(
 name="standard-bumpkin",
 py_modules=["bumpkin"],
 author="Fred Heidrich",
 url="https://github.com/fredheidrich/bumpkin",
 author_email="fredheidrich@gmail.com",
 version=__version__,
 description="Automatic versioning and changelog generation from git commits.",
 long_description=long_description,
 long_description_content_type="text/markdown",
 python_requires=">=3.6",
 packages=setuptools.find_packages(where="code"),
 package_dir={"": "code"},
 install_requires=[],
 classifiers = [
  "Programming Language :: Python",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.9",
  "Development Status :: 3 - Alpha",
  # "Development Status :: 4 - Beta",
  # "Development Status :: 5 - Production/Stable",
  "Environment :: Other Environment",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  "Topic :: Software Development :: Pre-processors",
  "Topic :: Software Development :: Libraries :: Python Modules",
  "Topic :: Software Development :: Code Generators",
 ]
)
