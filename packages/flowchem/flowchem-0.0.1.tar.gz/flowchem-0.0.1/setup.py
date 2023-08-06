import setuptools
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="flowchem",
    version="0.0.1",
    author="Dario Cambié, Jakob Wolf",
    author_email="dario.cambie@mpikg.mpg.de, jakob.wolf@mpikg.mpg.de",
    description="Flowchem is a python library to control a variety of instruments commonly found in chemistry labs.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cambiegroup/flowchem",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Chemistry"
    ],
    install_requires=[
        "pyserial",
        "pyserial-asyncio",
        "pint",
        "pandas",
        "scipy",
        "numpy",
        "opcua",
        "asyncua",
        "phidget22",
        "getmac",
        "lmfit",
        "nmrglue",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["flowchem=flowchem.cli:main"]},
)
