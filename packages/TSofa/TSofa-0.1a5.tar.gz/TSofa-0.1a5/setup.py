# Standard library imports.
import os

# Setuptools package imports.
from setuptools import setup

# Read the README.rst file for the 'long_description' argument given
# to the setup function.
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# Allow setup.py to be run from any path.
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name = 'TSofa',
    version = '0.1a5',
    packages = ['tsofa', 'tsofa._views'],
    entry_points = {'console_scripts': [
        'tsofa-d-doc-day = tsofa._views._d_doc_day:main',
        'tsofa-d-rpt-day = tsofa._views._d_rpt_day:main',
        'tsofa-d-elm-day = tsofa._views._d_elm_day:main',
        'tsofa-s-atr-day = tsofa._views._s_atr_day:main',
        'tsofa-d-doc-sec = tsofa._views._d_doc_sec:main',
        'tsofa-d-rpt-sec = tsofa._views._d_rpt_sec:main',
        'tsofa-d-elm-sec = tsofa._views._d_elm_sec:main',
        'tsofa-s-atr-sec = tsofa._views._s_atr_sec:main',
        'tsofa-d-doc-mls = tsofa._views._d_doc_mls:main',
        'tsofa-d-rpt-mls = tsofa._views._d_rpt_mls:main',
        'tsofa-d-elm-mls = tsofa._views._d_elm_mls:main',
        'tsofa-s-atr-mls = tsofa._views._s_atr_mls:main']},
    install_requires = [
        'pytz >= 2020.4', 'requests <= 2.22.0', 'Two-Percent >= 3.1'],
    license = 'BSD License',
    description = 'This package contains the reference CouchDB views for '\
        + 'well formatted timeseries data, the Python functionality to '\
        + 'retrieve data from those views, and functionality to process '\
        + 'the output.',
    long_description = README,
    url = 'https://bitbucket.org/notequal/tsofa/',
    author = 'Stanley Engle',
    author_email = 'stan.engle@gmail.com',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'],)

