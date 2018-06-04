from distutils.core import setup, Extension

controlsModule = Extension('controls',
    sources = ['controls.cpp'],
    include_dirs = ['/usr/include/irrlicht'],
    libraries = ['Irrlicht'],
    # library_dirs = ['/usr/local/lib'],
)

setup (name = 'controls',
    version = '1.0',
    description = 'Python interface for C++ methods controlling the 3D view.',
    ext_modules = [controlsModule],
)