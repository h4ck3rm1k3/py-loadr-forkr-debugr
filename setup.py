"""A setuptools based setup module for the py-loadr-forkr-debugr
"""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'Readme.md'), encoding='utf-8') as f:
        long_description = f.read()

name = 'py-loadr-forkr-debugr'
setup(
    name=name,
    version='0.0.1',

    description='Forking toolkit for iterativly testing slow loading code and data',
    long_description=long_description,
    url='https://github.com/h4ck3rm1k3/py-loadr-forkr-debugr',
    
    author='James Michael DuPont',
    author_email='jamesmikedupont+py-loadr-forkr-debugr@gmail.com',

    # Choose your license
    license='GPLV3',

    classifiers=[
        'Development Status :: 3 - Alpha',       
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GPLv3',
        
        'Programming Language :: Python :: 2.7',
        
    ],
    keywords='nose fork debug loader inotify',
    py_modules=["forkr"],   
    install_requires=['nose','pyinotify'],

    
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    #data_files=[('my_data', ['data/data_file'])],

    entry_points={
        'console_scripts': [
            'forkr=forkr:main',
        ],
    },
)
