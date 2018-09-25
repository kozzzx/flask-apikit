# -*- coding: utf-8 -*-
"""
Flask-APIKit
-------------

Build Restful API with Flask Quickly.
"""
from setuptools import setup, find_packages

setup(
    name='Flask-APIKit',
    version='0.0.5',
    url='https://github.com/kozzzx/flask-apikit',
    license='BSD',
    author='kozzzx',
    author_email='kozzzx@qq.com',
    description='Build Restful API with Flask Quickly.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=1.0', 'marshmallow==3.0.0b8'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
