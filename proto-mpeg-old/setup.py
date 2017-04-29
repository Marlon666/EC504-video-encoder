from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy

extensions = [
    Extension('proto_mpeg_x', ['proto_mpeg_x.pyx'],
              include_dirs=[numpy.get_include()]
              ),
    Extension('proto_mpeg_computation', ['proto_mpeg_computation.pyx'],
              include_dirs=[numpy.get_include()],
              extra_compile_args=["-O3"],
              ),
]

setup(
    name = "proto_mpeg_x",
    #ext_modules = cythonize('dct.pyx', include_path=[numpy.get_include()]),
    ext_modules = cythonize(extensions)
)

# Run this build process by doing: python3 setup.py build_ext --inplace