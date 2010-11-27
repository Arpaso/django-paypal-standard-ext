### -*- coding: utf-8 -*- ####################################################
"""
Configuration file used by setuptools. It creates 'egg', install all dependencies.
"""

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

#Dependencies - python eggs
install_requires = [
        'setuptools',
        'Django',
        'django-native-tags',
        'django-paypal',
]

#Execute function to handle setuptools functionality
setup(name="paypal-standard-ext",
            version="0.1",
            description="Paypal standard payment extension",
            long_description=read('README'),
            packages=find_packages('src'),
            package_dir={'': 'src'},
            include_package_data=True,
            zip_safe=True,
            install_requires=install_requires,
)