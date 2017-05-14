# -*- coding: utf-8 -*-
"""
Flask-ApiKit
-------------

Build Restful Api with Flask Quickly.
"""
from setuptools import setup

setup(
    name='Flask-ApiKit',
    version='0.1.0',
    # url='',
    license='BSD',
    author='kozzzx',
    author_email='kozzzx@qq.com',
    description='Build Restful Api with Flask Quickly.',
    long_description=__doc__,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask', 'marshmallow'
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
