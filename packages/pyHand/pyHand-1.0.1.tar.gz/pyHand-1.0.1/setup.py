from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.1'
DESCRIPTION = 'pyHand'
LONG_DESCRIPTION = 'A package which converts text to handwritten' \
                   '' \
                   'we need to first import the package - import pyHand' \
                   'then to get to know the information regarding this package you need to use the following command - pyHand.info()' \
                   'for converting you text to handwritten you will use the following command - pyHand.write("Sample Text")' \
                   '' \
                   'then it will ask you to ive the file name : ' \
                   'then you can find the handwritten text in png file with name you gave above' \
                   '' \
                   '@SujithSouryaYedida'
# Setting up
setup(
    name="pyHand",
    version=VERSION,
    author="SujithSouryaYedida",
    author_email="sujithsourya.yedida@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['colorama','pyfiglet','pywhatkit'],
    keywords=['handwritten', 'python', 'hand', 'text', 'SujithSouryaYedida','py','text to handwritten','write','written','pip'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)