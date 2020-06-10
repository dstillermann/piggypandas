import setuptools

with open('README.md', 'r') as fh:
    long_description: str = fh.read()

with open('requirements.txt', 'r') as fh:
    install_requires: list = [line.strip() for line in fh]

setuptools.setup(
    name="piggypandas",
    version="0.0.6",
    author="Dmitry Stillermannm",
    author_email="dmitry@stillermann.com",
    description="A few helpers for more efficient pandas work",
    long_description=long_description,
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
    python_requires='>=3.6',
    install_requires=install_requires
)
