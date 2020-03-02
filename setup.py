#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='nd2tif',
      version='0.1.1',
      description='Compress nd2 into multi-dimentional tiff',
      author='Andrey Aristov',
      author_email='aaristov@pasteur.fr',
      url='https://gitlab.pasteur.fr/aaristov/nd2shrink',
      install_requires=[
            'numpy', 
            'scikit-image', 
            'pims_nd2 @ git+https://github.com/aaristov/pims_nd2.git', 
            'pytest', 
            'tifffile', 
            'tqdm'
      ],
      python_requires=">=3.8",
      packages=find_packages(),
     )