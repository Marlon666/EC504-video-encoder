from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = "Hello world app",
    ext_modules = cythonize('hello.pyx'),
)

'''
How does this work?
1. The hello.pyx file is a module with python code that will be converted to c code and compiled
2. This file (setup.py) takes the .pyx file, does the c conversion, compiles, and builds a module
3. Run this build process by doing: python3 setup.py build_ext --inplace
4. You can then import the package 'hello' as you would any other package.
'''