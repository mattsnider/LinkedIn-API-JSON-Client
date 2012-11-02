import os, sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# README is required for distribution, but README.md is required for github,
#   so create README temporarily
os.system('cp %s/README.md %s/README.txt' % (ROOT_DIR, ROOT_DIR))

sdict = dict(
    name = 'linkedin-api-json-client',
    packages = ['linkedin_json_client'],
    version='.'.join(map(str, __import__('linkedin_json_client').__version__)),
    description = 'Python API for interacting with LinkedIn API.',
    long_description=open('README.md').read(),
    url = 'https://github.com/mattsnider/LinkedIn-API-JSON-Client',
    author = 'Matt Snider',
    author_email = 'admin@mattsnider.com',
    maintainer = 'Matt Snider',
    maintainer_email = 'admin@mattsnider.com',
    keywords = ['linkedin', 'api'],
    license = 'MIT',
    install_requires=[
        'mock',
        'oauth2',
        'simplejson'
    ],
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

# cleanup README
os.remove('%s/README.txt' % ROOT_DIR)