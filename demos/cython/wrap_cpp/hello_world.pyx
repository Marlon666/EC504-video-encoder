# distutils: language = c++
# distutils: sources = hello_world.cpp

cdef extern from 'hello_world.cpp':
    int add(int, int)

# Run this build process by doing: python3 setup.py build_ext --inplace