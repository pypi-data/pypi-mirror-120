import os
try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

here = os.path.abspath( os.path.dirname( __file__ ) )
README = open(os.path.join( here, 'README.rst' ) ).read()

setup(
    name='chibi_donkey',
    version='1.0.1',
    description='library for proccess the format double undescore',
    long_description=README,
    license='',
    author='dem4ply',
    author_email='',
    packages=find_packages(),
    install_requires=[],
    dependency_links = [],
    url='https://github.com/dem4ply/chibi_donkey',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ] )
