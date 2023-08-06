from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.4'
DESCRIPTION = 'Utils for sparta lab - hussam'
LONG_DESCRIPTION = 'Get months'

# Setting up
setup(
    name="lab317",
    version=VERSION,
    author="Hussam Habib",
    author_email="hussam-habib@uiowa.edu",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['datetime'],
    keywords=['utilities'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
