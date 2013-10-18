from distutils.core import setup
import sys

import everydo 

kw = dict(
    name = 'everydo',
    version = everydo.__version__,
    description = 'Everydo OAuth 2 API Python SDK',
    long_description = open('README', 'r').read(),
    author = 'Chen Weihong',
    author_email = 'whchen1080@gmail.com',
    url = 'https://github.com/michaelliao/sinaweibopy',
    download_url = 'https://github.com/michaelliao/sinaweibopy',
    py_modules = ['everydo'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

setup(**kw)
