
import io
import os
import re

from setuptools import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


with io.open('querybulletin/version.py', 'rt', encoding='utf-8') as f:
    version = re.search(r"__version__ = '(.*?)'", f.read()).group(1)


description = 'Simple Python library to query seismic bulletin database'

setup(
    name='bpptkg-querybulletin',
    version=version,
    description=description,
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    author='BPPTKG',
    author_email='bpptkg@esdm.go.id',
    url='https://github.com/bpptkg/bpptkg-querybulletin',
    zip_safe=True,
    packages=['querybulletin'],
    entry_points={
        'console_scripts': [
            'querybulletin = querybulletin.cli:main',
        ]
    },
    install_requires=['sqlalchemy', 'pandas'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)
