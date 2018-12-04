from distutils.core import setup
from Cython.Build import cythonize
from setuptools import setup, find_packages

setup(name='pythonGroupMsg',
      ext_modules = cythonize("lib.py",language_level=3),
      version='0.0.1',
      description='This is a packet that broadcasts redis multiple queues',
      url='https://github.com/zhenruyan/pythonGroupMsg',
      author='zhenruyan',
      author_email='baiyangwangzhan@hotmail.com',
      license='WTFPL',
      packages=find_packages(),
      zip_safe=False,
      platforms=["all"],
      long_description=open('README.rst').read(),
classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ]
      )