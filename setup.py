#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
        name='aurchk',
        version='0.0.1',
        description='A simple tool to check updates for AUR packages.',
        author='OriginCode',
        author_email='self@origincode.me',
        url='https://github.com/OriginCode/aurchk',
        packages=find_packages(),
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: POSIX :: Linux',
            'Development Status :: 3 - Alpha',
            'Natural Language :: English',
            'Topic :: Utilities',
            'Intended Audience :: End Users/Desktop'
        ],
        install_requires=[
            'pyalpm',
            'GitPython',
            'aiohttp',
            'termcolor'
        ],
        python_requires='>=3.8'
)