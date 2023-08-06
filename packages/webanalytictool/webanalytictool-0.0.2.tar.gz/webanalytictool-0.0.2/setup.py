from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="webanalytictool",
    version="0.0.2",
    description="A package for analysing webpages",
    py_modules=["analytic"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/komus/webpage-analysis-tool",
    author="Oyindolapo Komolafe",
    author_email="",

    install_requires = [
        "beautifulsoup4 ~= 4.9.3",
        "requests ~= 2.25.1",
        "pandas ~= 1.3.0",
    ],

    extras_require = {
        "dev": [
            "pytest >= 3.7",
        ],
    },
)