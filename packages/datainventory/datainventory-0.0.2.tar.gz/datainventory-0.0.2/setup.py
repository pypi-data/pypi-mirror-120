"""Setup file for Data Inventory."""

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.rst").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="datainventory",
    version="0.0.2",
    description="Data Inventory",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/iot-spectator/datainventory",
    author="IoT Spectator",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="image and video database",
    packages=setuptools.find_packages(exclude=["diagram", "examples", "tests"]),
    python_requires=">=3.7",
)
