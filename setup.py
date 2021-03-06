# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages


setup(
    name='django-flow',
    version='0.1.1',
    author=u'Madhukar Mishra, serafinjp@gmail.com(original author)',
    author_email='madhukar93@gmail.com, jean-philippe serafin',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/madhukar93/django-flow/',
    license='MIT licence',
    description='Django resumable uploads',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django>=1.4',
        'python-magic',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
