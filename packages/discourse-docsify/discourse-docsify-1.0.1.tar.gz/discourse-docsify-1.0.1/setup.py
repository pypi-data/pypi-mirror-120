#!/usr/bin/env python
from setuptools import find_packages, setup

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(
    name="discourse-docsify",
    version='1.0.1',
    url="https://github.com/guipenedo/discourse-docsify",
    license="MIT",
    author="Guilherme Penedo",
    author_email="nostrumg@gmail.com",
    description="Flask extension to add docsify (documentation) sourced from discourse (forum) content.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={
        'discourse_docsify.static': ['*'],
    },
    python_requires=">=3.5",
    install_requires=[
        "Flask>=1.0.2",
        "requests",
        "redis",
        "python-dateutil",
        "humanize",
    ],
)
