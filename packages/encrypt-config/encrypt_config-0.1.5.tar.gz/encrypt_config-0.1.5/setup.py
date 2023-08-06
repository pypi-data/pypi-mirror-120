#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['cryptography==3.4.8']


test_requirements = ['pytest>=3', ]

setup(
    author="Luis C. Berrocal",
    author_email='luis.berrocal.1942@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Encrypt and decrypt information in configuration files.",
    entry_points={
        'console_scripts': [
            'encrypt_config=encrypt_config.cli:main',
        ],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='encrypt_config',
    name='encrypt_config',
    packages=find_packages(include=['encrypt_config', 'encrypt_config.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/luiscberrocal/encrypt_config',
    version='0.1.5',
    zip_safe=False,
)
