from setuptools import setup
from lazy_ips import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='lazy_ips',
    version=__version__,
    description='IPS patcher with CLI user interface.',
    long_description=long_description,
    author='Boris Timofeev',
    author_email='btimofeev@emunix.org',
    url='https://github.com/richardhob/lazy_ips',
    license='GNU GPLv3',
    packages=['lazy_ips',
              'lazy_ips.patch'],
    entry_points={
        "console_scripts": ["lazy-ips-cli=lazy_ips.cli:main"],
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Topic :: Utilities',
    ]
)
