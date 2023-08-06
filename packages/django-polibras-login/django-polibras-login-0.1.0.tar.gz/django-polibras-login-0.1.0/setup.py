from setuptools import setup, find_packages
from pathlib import Path


requires = ['django-allauth>=0.45.0,<1.0.0', 'django-environ']

this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name='django-polibras-login',
    packages=find_packages(),
    version='0.1.0',
    description='A Django app to realize login with google on polibras environments.',
    long_description=long_description,
    url='https://polibrassoftware.com.br/',
    author='Andre Conjo',
    author_email='andre.conjo@polibrassoftware.com.br',
    license='BSD-3-Clause',
    classifiers=['Framework :: Django :: 3.0', 'License :: OSI Approved :: BSD License', 'Programming Language :: Python', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3 :: Only'],
    install_requires=requires
    )

