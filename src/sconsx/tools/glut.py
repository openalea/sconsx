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
""" OpenGL configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"


import os, sys
from openalea.sconsx.config import *

exists = os.path.exists

class GLUT:
   def __init__(self, config):
      self.name = 'glut'
      self.config = config
      self._default = {}


   def default(self):
       if isinstance(platform, Win32):
           #MVSdir = r'C:\Program Files\Microsoft Visual Studio\VC98'
           MVSdir = r'C:\Program Files\Microsoft Platform SDK'
           self._default['msvc_include'] = pj(MVSdir, 'Include')
           self._default['msvc_lib'] = pj(MVSdir, 'Lib')
        
           mgw_dir = find_executable_path_from_env("mingw32-make.exe", strip_bin=True)           
           mgw_dir = mgw_dir or r'C:\MinGW'
           self._default['mgw_include'] = pj(mgw_dir, 'include', 'GL')
           self._default['mgw_lib'] = pj(mgw_dir, 'lib')
        
           self._default['include'] = self._default['msvc_include']
           self._default['lib'] = self._default['msvc_lib']
       elif isinstance(platform, Posix):
           if exists ('/usr/include/GL/glut.h'):
               self._default['include'] = '/usr/include'
               self._default['lib'] = '/usr/lib'
           else: 
               self._default['include'] = '/usr/X11R6/include'
               self._default['lib'] = '/usr/X11R6/lib'


   def option( self, opts):
       self.default()

       if isinstance(platform, Darwin):
           opts.AddVariables(
                           ('glut_includes', 'GLUT include files',  self._default['include']),
                           ('glut_framework_path', 'GLUT framework path', '/System/Library/Frameworks'),
                           ('glut_frameworks', 'GLUT frameworks', ['GLUT'])
                           )
       else:
           opts.AddVariables(
                            ('glut_includes', 'GLUT include files',  self._default['include']),
                            ('glut_lib', 'GLUT library path', self._default['lib'])
                            )


   def update(self, env):
      """ Update the environment with specific flags """
      if isinstance(platform, Darwin):
          env.AppendUnique(CPPPATH=[env['glut_includes']])
          env.AppendUnique(LINKFLAGS="-F%s"%str(env['glut_framework_path']))
          for fmk in env['glut_frameworks']:
              env.Append(LINKFLAGS=['-framework',str(fmk)])
          return
      if env.get('compiler', 'mingw') == 'mingw':
          if env['glut_includes'] == self._default['msvc_include']:
              env['glut_includes'] = self._default['mgw_include']
          if env['glut_lib'] == self._default['msvc_lib']:
              env['glut_lib'] = self._default['mgw_lib']

      env.AppendUnique(CPPPATH=[env['glut_includes']])
      env.AppendUnique(LIBPATH=[env['glut_lib']])

      if isinstance(platform, Cygwin):
          env.AppendUnique(LIBS=['glut32'])
      elif isinstance(platform, Posix):
          env.AppendUnique(LIBS=['glut'])
      elif isinstance(platform, Win32):
          env.AppendUnique(LIBS=['glut32'])


   def configure(self, config):
      if not config.conf.CheckLibWithHeader('GL',['GL/glut.h'], 'c++', autoadd = 0):
         print "Error: glut.h not found, probably failure in automatic opengl detection"
         sys.exit(-1)


def create(config):
   " Create glut tool "
   glut = GLUT(config)

   return glut

