from distutils.core import setup
from Cython.Build import cythonize
setup(
    name='lib',
    ext_modules=cythonize('clib.pyx')
)

