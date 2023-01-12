#!/usr/bin/env python3

# ./setup.py build && ./setup.py install


from setuptools import setup, find_packages

def get_readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='texdown',
    version='0.1',
    description='Converts specially formated markdown to latex.',
    long_description=get_readme(),
    classifiers=[
      'Programming Language :: Python :: 3.10',
    ],
    keywords='markdown latex tex',
    url='https://github.com/ckotecky/texdown',
    # install_requires=[
    #     'jinja2',
    #     'PyYAML',
    #     'roman',
    # ],
    # include_package_data=True,
    # zip_safe=False,
    packages=find_packages(),
    include_package_data = True,
    entry_points={
        'console_scripts': [
            'texdown=source.texdown:main',
        ],
    },
)
