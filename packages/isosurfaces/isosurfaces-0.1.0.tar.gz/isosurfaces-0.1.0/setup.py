import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (
    (HERE / "README.md")
    .read_text()
    .replace(
        "assets/demo.svg",
        "https://cdn.jsdelivr.net/gh/jared-hughes/isosurfaces/assets/demo.svg",
    )
)

# This call to setup() does all the work
setup(
    name="isosurfaces",
    version="0.1.0",
    description="Construct isolines/isosurfaces over a 2D/3D scalar field defined by a function (not a uniform grid)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jared-hughes/isosurfaces",
    author="Jared Hughes",
    author_email="jahughes.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["isosurfaces"],
    include_package_data=True,
    install_requires=["numpy"],
)
