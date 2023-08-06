from setuptools import setup
from os import path

requirements = [
    'google-api-python-client==2.20.0',
    'google-auth-httplib2==0.1.0',
    'google-auth-oauthlib==0.4.6',
    'pytz',
]
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='indonesia_holiday',
    version='1.0',
    packages=['indonesia_holiday',],
    license='MIT',
    author="ahmadcahyana",
    author_email="ahmadcahyana@outlook.com",
    description="python module to check indonesia holiday calendar",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="holiday indonesia calendar",
    url="https://github.com/ahmadcahyana/indonesia_holiday",
    install_requires=requirements,
)