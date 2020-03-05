#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="nd2tif",
    version="0.3.0-dev",
    description="Compress nd2 into multi-dimensional tiff",
    author="Andrey Aristov",
    author_email="aaristov@pasteur.fr",
    url="https://gitlab.pasteur.fr/aaristov/nd2shrink",
    install_requires=[
        "numpy",
        "scipy",
        "opencv-python",
        "scikit-image",
        "pims_nd2 @ git+https://github.com/aaristov/pims_nd2.git",
        "nd2reader",
        "pytest",
        "tifffile",
        "tqdm",
        "pandas",
    ],
    python_requires=">=3.8",
    packages=find_packages(),
)
