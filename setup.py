#!/usr/bin/env python
from os import path

ROOT_DIR = path.abspath(path.dirname(__file__))

def get_deps():
    f = open(path.join(ROOT_DIR, "requirements.pip"), 'r')
    return [l[:-1] for l in f.readlines()]

sdict = dict(
    name = 'linkedin-api-json-client',
    packages = ['linkedin_json_client'],
    version='.'.join(map(str, __import__('linkedin_json_client').__version__)),
    description = 'Python API for interacting with LinkedIn API.',
    long_description=open('README.rst').read(),
    url = 'https://github.com/mattsnider/LinkedIn-API-JSON-Client',
    author = 'Matt Snider',
    author_email = 'adming@mattsnider.com',
    maintainer = 'Matt Snider',
    maintainer_email = 'adming@mattsnider.com',
    keywords = ['linkedin', 'api'],
    license = 'MIT',
    install_requires=get_deps(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)

from distutils.core import setup
setup(**sdict)