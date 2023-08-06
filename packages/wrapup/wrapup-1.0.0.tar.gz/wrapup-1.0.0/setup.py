import setuptools

with open("readme.md", "r") as fh:
    project_description = fh.read()

setuptools.setup(
    name="wrapup",
    version="1.0.0",
    description="A library that is used to remove print statements or "
    "converting quotes in python files (if present) in a folder",
    author="Faizan Mombasawala",
    long_description=project_description,
    long_description_content_type="text/markdown",
    author_email="mombasawalafaizan6@gmail.com",
    packages=["wrapup"],
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    keywords="library, format, remove prints, print, ",
    python_requires=">=3.6, <4",
)
