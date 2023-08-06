#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import codecs


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='django-multicurrency',
    version='0.1.2',
    license='Apache 2.0',

    requires=[
        'Django (>=3.0)',
    ],

    description='Simple Django multicurrency field',
    long_description=long_description,
    long_description_content_type="text/markdown",

    author='Neural Dynamics',
    author_email='neuraldynamics.web@gmail.com',

    url='https://github.com/NeuralDynamicsWeb/django-multicurrency',
    download_url = 'https://github.com/NeuralDynamicsWeb/django-multicurrency/archive/refs/tags/v_02.1.tar.gz',

    packages=find_packages(exclude=('example*',)),
    include_package_data=True,

    keywords = ['Django', 'Multicurrency'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)