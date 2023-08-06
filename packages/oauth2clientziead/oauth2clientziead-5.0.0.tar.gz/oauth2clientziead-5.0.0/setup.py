
from __future__ import print_function

import sys

from setuptools import find_packages
from setuptools import setup

import oauth2clientziead

if sys.version_info < (2, 7):
    print('oauth2clientziead requires python2 version >= 2.7.', file=sys.stderr)
    sys.exit(1)
if (3, 1) <= sys.version_info < (3, 4):
    print('oauth2clientziead requires python3 version >= 3.4.', file=sys.stderr)
    sys.exit(1)

install_requires = [
    'httplib2>=0.9.1',
    'pyasn1>=0.1.7',
    'pyasn1-modules>=0.0.5',
    'rsa>=3.1.4',
    'six>=1.6.1',
]

long_desc = """
oauth2clientziead is a client library for OAuth 2.0.

Note: oauth2clientziead is now deprecated. No more features will be added to the
    libraries and the core team is turning down support. We recommend you use
    `google-auth <https://google-auth.readthedocs.io>`__ and
    `oauthlib <http://oauthlib.readthedocs.io/>`__.
"""

version = '5.0.0'
setup(
    name='oauth2clientziead',
    version=version,
    description='client library',
    long_description=long_desc,
    author='ZSK',
    author_email='zshabkalieh@gmail.com',
    url='https://github.com/zieadshabkalieh/oauth2clientziead',
    install_requires=install_requires,
    packages=find_packages(exclude=('tests*',)),
    keywords='google oauth 2.0 http client',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
