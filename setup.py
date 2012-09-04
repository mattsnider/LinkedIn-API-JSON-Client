#!/usr/bin/env python

sdict = dict(
    name = 'linkedin-api-json-client',
    packages = ['linkedin_json_client'],
    version = '0.1.0',
    description = 'Python API for interacting with LinkedIn API.',
    long_description = 'Python API for interacting with LinkedIn API',
    url = 'https://github.com/mattsnider/LinkedIn-API-JSON-Client',
    author = 'Matt Snider',
    author_email = 'adming@mattsnider.com',
    maintainer = 'Matt Snider',
    maintainer_email = 'adming@mattsnider.com',
    keywords = ['linkedin', 'api'],
    license = 'MIT',
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