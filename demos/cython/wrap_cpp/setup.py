from distutils.core import setup
from Cython.Build import cythonize

setup(name="testapp",
      ext_modules = cythonize('*.pyx'),
      )