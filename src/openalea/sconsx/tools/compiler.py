# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------
""" Build directory configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"


from SCons.Variables import PathVariable 
from SCons.Variables import BoolVariable 
from SCons.Variables import EnumVariable 
from SCons.Variables import Variables
from SCons.Util import Split, WhereIs

import os, sys
from openalea.sconsx.config import *

MsvcVersion = {
    1929 : '16.10', 
    1928 : '16.8', 
    1927 : '16.7', 
    1926 : '16.6', 
    1925 : '16.5', 
    1924 : '16.4', 
    1923 : '16.3', 
    1922 : '16.2', 
    1921 : '16.1', 
    1920 : '16.0', 
    1916 : '15.9', 
    1915 : '15.8', 
    1914 : '15.7', 
    1913 : '15.6', 
    1912 : '15.5', 
    1911 : '15.3', 
    1910 : '15.0', 
    1900 : '14.0', 
    1800 : '12.0', 
    1700 : '11.0', 
    1600 : '10.0', 
    1500 : '9.0', 
    1400 : '8.0', 
    1310 : '7.1', 
    1300 : '7.0', 
    1200 : '6.0'
     
}

def get_default_msvc():
    import platform
    version = platform.python_compiler().split()[1][2:]
    return MsvcVersion[int(version)]



class Compiler:

    def __init__(self, config):
        self.name = 'compiler'
        self.config = config
        self._default = {}


    def default(self):

        self._default['debug'] = False
        self._default['warnings'] = False
        self._default['static'] = False

        if isinstance(platform, Posix):
            compilers = ['gcc']
            libs_suffix = ''
        elif isinstance(platform, Win32):
            if CONDA_ENV :
                compilers = ['msvc','mingw']
            else:
                compilers = ['mingw', 'msvc']
            libs_suffix = '-vc90'
        else:
            raise Exception("Add a compiler support for your os !!!")

        self._default['compilers'] = compilers
        self._default['libs_suffix'] = libs_suffix


    def option( self, opts):

        self.default()

        opts.Add(BoolVariable('debug', 
                          'compilation in a debug mode',
                          self._default['debug']))
        opts.Add(BoolVariable('warnings',
                          'compilation with -Wall and similar',
                          self._default['warnings']))
        opts.Add(BoolVariable('static',
                          '',
                          self._default['static']))

        compilers = self._default['compilers']
        default_compiler = compilers[0]
        opts.Add(EnumVariable('compiler',
                          'compiler tool used for the build',
                          default_compiler,
                          compilers))
        opts.Add('compiler_libs_suffix', 
               'Library suffix name like -vc80 or -mgw',
               self._default['libs_suffix'])
                           
        opts.Add('rpath', 'A list of paths to search for shared libraries')

        opts.Add('EXTRA_CCFLAGS', 'Specific user flags for c compiler', '')
        opts.Add('EXTRA_CXXFLAGS', 'Specific user flags for c++ compiler', '')
        opts.Add('EXTRA_CPPDEFINES', 'Specific c++ defines', '')
        opts.Add('EXTRA_LINKFLAGS', 'Specific user flags for c++ linker', '')
        opts.Add('EXTRA_CPPPATH', 'Specific user include path', '')
        opts.Add('EXTRA_LIBPATH', 'Specific user library path', '')
        opts.Add('EXTRA_LIBS', 'Specific user libraries', '')

        if isinstance(platform, Win32):
            opts.Add(EnumVariable('TARGET_ARCH', 'Target Architecture','amd64' if is_64bit_environment() else 'x86', allowed_values=('x86','amd64','i386','emt64','x86_64','ia64')))
            opts.Add(EnumVariable('MSVC_VERSION', 'Version ','' if not is_conda() else get_default_msvc(), allowed_values=sorted(MsvcVersion.values())+['']))

    def update(self, env):
        """ Update the environment with specific flags """

        # Set the compiler
        compiler_name = env['compiler']

        self.config.add_tool(compiler_name)
      
        if isinstance(platform, Cygwin):
            env.AppendUnique(CPPDEFINES = 'SYSTEM_IS__CYGWIN')
        elif isinstance(platform, Win32):
            env.AppendUnique(CPPDEFINES = 'WIN32')
            libs_suffix = env['compiler_libs_suffix']
            if compiler_name == 'mingw' and '-vc' in libs_suffix:
                env['compiler_libs_suffix'] = '-mgw'

        env.Append(RPATH=Split('$rpath'))
        env.Append(CCFLAGS=Split(env['EXTRA_CCFLAGS']))
        env.Append(CXXFLAGS=Split(env['EXTRA_CXXFLAGS']))
        env.Append(CPPDEFINES=Split(env['EXTRA_CPPDEFINES']))
        env.Append(LINKFLAGS=Split(env['EXTRA_LINKFLAGS']))
        env.Append(CPPPATH=Split(env['EXTRA_CPPPATH']))
        env.Append(LIBPATH=Split(env['EXTRA_LIBPATH']))
        env.Append(LIBS=Split(env['EXTRA_LIBS']))


    def configure(self, config):
        pass

def create(config):
     " Create compiler tool "
     compiler = Compiler(config)

     return compiler

