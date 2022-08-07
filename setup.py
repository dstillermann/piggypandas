import setuptools
import re


def _read_long_description() -> str:
    with open('README.md', 'r') as fh:
        return fh.read()


def _read_install_requires() -> list:
    with open('requirements.txt', 'r') as fh:
        return [line.strip() for line in fh]


def _read_version() -> str:
    ver_file: str = 'piggypandas/_version.py'
    with open(ver_file, 'rt') as fh:
        text: str = fh.read()
        m = re.search(r'__version__\s*=\s*[\'\"]([^\'\"]*)[\'\"]', text, re.MULTILINE)
        if m:
            return m.group(1)
        else:
            raise RuntimeError(f"Unable to locate version string in \"{ver_file}\"")


setuptools.setup(
    name="piggypandas",
    version=_read_version(),
    author="Dmitry Stillermannm",
    author_email="dmitry@stillermann.com",
    description="A few helpers for more efficient pandas work",
    long_description=_read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/dstillermann/piggypandas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.9',
    install_requires=_read_install_requires()
)
