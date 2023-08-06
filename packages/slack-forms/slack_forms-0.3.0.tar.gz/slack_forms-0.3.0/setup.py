#!/usr/bin/env python

"""The setup script."""

from typing import List
from setuptools import setup, find_packages  # type: ignore

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements: List[str] = requirements_file.read().split('\n')

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Rod Morison",
    author_email='rmorison@aspiration.com',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    description="Django forms icing on the Slack App cake",
    install_requires=requirements,
    license="ISC license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='slack_forms',
    name='slack_forms',
    packages=find_packages(include=['slack_forms', 'slack_forms.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aspiration-labs/slack_forms',
    version='0.3.0',
    zip_safe=False,
)
