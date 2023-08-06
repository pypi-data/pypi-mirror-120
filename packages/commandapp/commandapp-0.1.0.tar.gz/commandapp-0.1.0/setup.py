import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__author__ = "PlayerG9"
__copyright__ = "Copyright 2021, PlayerG9"
__credits__ = ["PlayerG9"]
__license__ = "MIT"
__version_info__ = (0,1,0)
__version__ = '.'.join(str(_) for _ in __version_info__)
__maintainer__ = "PlayerG9"
__email__ = None
__status__ = "Prototype"  # Prototype, Development, Production

setuptools.setup(
    name="commandapp",
    version=__version__,
    author=__author__,
    # author_email="author@example.com",
    description="tool to create a commandline application easily",
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
