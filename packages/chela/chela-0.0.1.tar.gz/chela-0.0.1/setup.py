import pathlib
from setuptools import setup
from setuptools import find_packages

# the difectory contaning this file
HERE = pathlib.Path(__file__).parent

# the text of the README file
README = (HERE / "README.md").read_text()

# setup
setup(
    name = "chela",
    version = "0.0.1",
    description = "Library to handle chemical formulas",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ClaudioPereti/chela",
    author = "Claudio Pereti",
    license = 'MIT',
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    package = ['chela'],
    include_package_data = True,
    install_requires = [
        'pandas',
        'numpy',
        'mendeleev',
        'pytest',
    ],
    entry_points = {
        "console_scripts":[
            "chela= chela.__main__:main"
        ]
    },
)
