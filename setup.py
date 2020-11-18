# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 11:30:00 2020

@author: Ruben
"""

from setuptools import setup

setup_args = dict(
    name="pygraphtec",
    version="0.1",
    url='http://github.com/isi-ies-group/pygraphtec',
    author="Ruben",
    author_email="ruben.nunez@upm.es",
    description="Pequeña librería que facilita la lectura de ficheros de datos en el FTP del datalogger Graphtec GL840",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Windows",
    ],
    python_requires='>=3.6',
    packages=['pygraphtec'],
    zip_safe=False,
    package_data={'': ['*.txt','*.yaml']},
    include_package_data=True,
)

install_requires = [
    'pandas',
    'datetime',
    'pathlib',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)

