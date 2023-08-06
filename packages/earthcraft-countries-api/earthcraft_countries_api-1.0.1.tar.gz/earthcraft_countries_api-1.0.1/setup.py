import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="earthcraft_countries_api",
    version="1.0.1",
    description="Countries API used by the EarthCraft bot",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://earthcraftmc.net/",
    author="FrenchFries8854",
    author_email="frenchfries8854@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["earthcraft_countries_api"],
    include_package_data=True,
    install_requires=["feedparser", "html2text"],
)
