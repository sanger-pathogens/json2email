import os
from setuptools import setup, find_packages
import multiprocessing

def readme():
  with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    return f.read()

setup(name='json2email',
      version='0.0.6',
      description='Takes a jinja2 template and some json and sends an email',
      long_description=readme(),
      url='https://github.com/sanger-pathogens/json2email',
      author='Ben Taylor',
      author_email='ben.taylor@sanger.ac.uk',
      scripts=['scripts/json2email'],
      include_package_data=True,
      install_requires=[
        'jinja2'
      ],
      test_suite='nose.collector',
      tests_require=[
        'nose',
        'mock'
      ],
      license='GPLv3',
      packages=find_packages(),
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Topic :: Communications :: Email",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities"
      ]
)
