#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'AWSIoTPythonSDK',
    'colour',
    'requests',
    'PyJWT==1.7.1',
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Thomas Reiser",
    author_email='reiser.thomas@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Home Automation'
    ],
    description="Simple and minimal Govee Home API client",
    install_requires=requirements,
    license="Apache Software License",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='govee_api2',
    name='govee_api2',
    packages=find_packages(include=['govee_api2', 'govee_api2.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/filipealvesdef/govee_api/tree/filipealves-setup-fixes',
    version='1.3.0',
    zip_safe=False,
)
