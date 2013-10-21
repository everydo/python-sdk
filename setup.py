from setuptools import setup, find_packages

kw = dict(
    name = 'everydo_client',
    version = '0.0.1',
    description = 'Everydo OAuth 2 API Python SDK',
    long_description = "laala",
    author = 'Chen Weihong',
    author_email = 'whchen1080@gmail.com',
    url = 'https://github.com/michaelliao/sinaweibopy',
    download_url = 'https://github.com/michaelliao/sinaweibopy',
    packages = find_packages(),
    install_requires = ['py-oauth2>=0.0.5'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

setup(**kw)
