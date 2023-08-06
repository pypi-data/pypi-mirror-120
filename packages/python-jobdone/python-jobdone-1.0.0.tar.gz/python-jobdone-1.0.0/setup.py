"""Setup script for realpython-reader"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="python-jobdone",
    version="1.0.0",
    description="This is unofficial python library for jobdone.net",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/krakiun/python-jobdone",
    author="krakiun",
    author_email="krakiun@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["jobdone"],
    include_package_data=True,
    install_requires=[
        "requests", "importlib_resources", "typing"
    ],
    entry_points={"console_scripts": ["realpython=reader.__main__:main"]},
)
