import pathlib
from setuptools import setup

# the directory containing this file
HERE = pathlib.Path(__file__).parent

# the text of the README
README = pathlib.Path('./README.md').read_text()

setup(
    name="cnnlite",
    version="0.0.1",
    description="Read today's CNN Lite articles",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/paulzuradzki/cnnlite",
    author="Paul Zuradzki",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        ],
    packages=["cnnlite"],
    include_package_data = True,
    install_requires=["requests", "beautifulsoup4"],
    #install_requires=["requests==2.26.0", "beautifulsoup4==4.9.3"],

    # entry_points is used to create scripts that call a function within your package
    # create a new script `scraper` that calls main() within the cnnlite/__main__.py file
    entry_points={
        "console_scripts": [
            "scraper=cnnlite.__main__:main"
        ]
    }
)