import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__author__ = "PlayerG9"
__version__ = "0.2.0"

setuptools.setup(
    name="commandapp",
    version=__version__,
    author=__author__,
    # author_email="author@example.com",
    description="library to create a commandline application easily",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PlayerG9/PyCommandApp",
    project_urls={
        "Author Github": "https://github.com/PlayerG9",
        "Bug Tracker": "https://github.com/PlayerG9/PyCommandApp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "commandapp"},
    packages=setuptools.find_packages(where="commandapp"),
    python_requires=">=3.6",
)
