# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = str(f.read())

# This call to setup() does all the work
setup(
    name="free_sms_otp",
    version="1.0.0",
    description="Library that allows you to generate and check sms otp codes for free",
    long_description_content_type="text/markdown",
    long_description="see https://github.com/QwertyQwertovich/free-sms-otp",
    url="https://github.com/QwertyQwertovich/free-sms-otp",
    author="Alexander Kharitonov",
    author_email="gametopsss@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["free_sms_otp"],
    include_package_data=True,
    install_requires=["requests"]
)