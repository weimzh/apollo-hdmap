# coding:utf-8

import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.command.build_py import build_py
from distutils.version import LooseVersion
from distutils.spawn import find_executable


# Find the Protocol Compiler.
if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
    protoc = os.environ['PROTOC']
elif os.path.exists('../bazel-bin/protoc'):
    protoc = '../bazel-bin/protoc'
elif os.path.exists('../bazel-bin/protoc.exe'):
    protoc = '../bazel-bin/protoc.exe'
elif os.path.exists('protoc'):
    protoc = '../protoc'
elif os.path.exists('protoc.exe'):
    protoc = '../protoc.exe'
elif os.path.exists('../vsprojects/Debug/protoc.exe'):
    protoc = '../vsprojects/Debug/protoc.exe'
elif os.path.exists('../vsprojects/Release/protoc.exe'):
    protoc = '../vsprojects/Release/protoc.exe'
else:
    protoc = find_executable('protoc')

def GenProto(source, require=True):
    """Generates a _pb2.py from the given .proto file.
    Does nothing if the output already exists and is newer than the input.
    Args:
        source: the .proto file path.
        require: if True, exit immediately when a path is not found.
    """

    if not require and not os.path.exists(source):
        return

    output = source.replace('.proto', '_pb2.py').replace('../src/', '')

    if (not os.path.exists(output) or
        (os.path.exists(source) and
         os.path.getmtime(source) > os.path.getmtime(output))):
        print('Generating %s...' % output)

    if not os.path.exists(source):
        sys.stderr.write("Can't find required file: %s\n" % source)
        sys.exit(-1)

    if protoc is None:
        sys.stderr.write(
            'protoc is not installed nor found in ../src.  Please compile it '
            'or install the binary package.\n')
        sys.exit(-1)

    protoc_command = [protoc, '-I./proto', '-I.', '--python_out=./apollo_hdmap', source]
    if subprocess.call(protoc_command) != 0:
        sys.exit(-1)


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]

        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)


class BuildPyCmd(build_py):
    """Custom build_py command for building the protobuf runtime."""

    def run(self):
        # Generate necessary .proto file if it doesn't exist.
        GenProto('./proto/error_code.proto')
        GenProto('./proto/geometry.proto')
        GenProto('./proto/header.proto')
        GenProto('./proto/map.proto')
        GenProto('./proto/map_clear_area.proto')
        GenProto('./proto/map_crosswalk.proto')
        GenProto('./proto/map_geometry.proto')
        GenProto('./proto/map_id.proto')
        GenProto('./proto/map_junction.proto')
        GenProto('./proto/map_lane.proto')
        GenProto('./proto/map_overlap.proto')
        GenProto('./proto/map_parking_space.proto')
        GenProto('./proto/map_pnc_junction.proto')
        GenProto('./proto/map_road.proto')
        GenProto('./proto/map_rsu.proto')
        GenProto('./proto/map_signal.proto')
        GenProto('./proto/map_speed_bump.proto')
        GenProto('./proto/map_speed_control.proto')
        GenProto('./proto/map_stop_sign.proto')
        GenProto('./proto/map_yield_sign.proto')
        GenProto('./proto/navigation.proto')
        GenProto('./proto/pnc_point.proto')
        # build_py is an old-style class, so super() doesn't work.
        build_py.run(self)

setup(
    name = 'apollo-hdmap',
    version = '7',
    description = 'standalone apollo hdmap module',
    author = 'Wei Mingzhi',
    author_email = 'whistler_wmz@users.sf.net',
    url = 'https://gitee.com/weimzh/apollo-hdmap/',
    packages = ['apollo_hdmap'],
    ext_modules = [CMakeExtension('apollo_hdmap_wrapper', '.')],
    cmdclass = dict(build_py=BuildPyCmd, build_ext=CMakeBuild),
    zip_safe = False,
)

