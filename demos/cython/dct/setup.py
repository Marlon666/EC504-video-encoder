from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension('dct', ['dct.pyx'],
              include_dirs=[numpy.get_include()]
              ),
]

setup(
    name = "dct",
    #ext_modules = cythonize('dct.pyx', include_path=[numpy.get_include()]),
    ext_modules = cythonize(extensions)
)

# Run this build process by doing: python3 setup.py build_ext --inplace