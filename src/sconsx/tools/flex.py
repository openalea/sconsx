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
""" Flex configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys
from openalea.sconsx.config import *


class Flex:
   def __init__(self, config):
      self.name = 'flex'
      self.config = config
      self._default = {}


   def default(self):

      if CONDA_ENV:
          if os.name == 'posix':
            base_dir = CONDA_LIBRARYPREFIX
          else:
            # On windows, the conda package providing flex (m2-flex) is located in Library/usr
            base_dir = os.path.join(CONDA_LIBRARYPREFIX, 'usr')
          self._default['bin'] = pj(base_dir, 'bin')
          self._default['include'] = pj(base_dir, 'include')
          if not isinstance(platform, Win32):
              self._default['libs'] = ['m','fl']
              self._default['libpath'] = pj(base_dir, 'lib')
      elif isinstance(platform, Win32):
         try:
              # Try to use openalea egg
              from openalea.deploy import get_base_dir
              base_dir = get_base_dir("bisonflex")
              self._default['bin'] = pj(base_dir, 'bin')
              self._default['include'] = pj(base_dir, 'include')
         except:
              self._default['bin'] = pj('C:\\', 'Tools', 'Bin')
              self._default['include'] = pj('C:\\', 'Tools', 'Include')

      elif isinstance(platform, Posix):
         self._default['bin'] = '/usr/bin'
         self._default['libpath'] = '/usr/lib'
         self._default['libs'] = ['m','fl']
         self._default['include'] = '/usr/include'


   def option( self, opts):

      self.default()

      opts.Add('flex_bin', 'Flex binary path',
                self._default['bin'])
      if not isinstance(platform, Win32):
          opts.Add('flex_libpath', 'Flex lib path',
                    self._default['libpath'])
      if not isinstance(platform, Win32):
          opts.Add('flex_libs', 'Flex libs',
                    self._default['libs'])
      opts.Add('flex_include', 'Flex include path',
                self._default['include'])


   def update(self, env):
      """ Update the environment with specific flags """

      if not isinstance(platform, Win32):
         env.AppendUnique(LIBS=env['flex_libs'])
         env.AppendUnique(LIBPATH=[env['flex_libpath']])
      env.AppendUnique(CPPPATH=[env['flex_include']])

      t = Tool('lex', toolpath=[getLocalPath()])
      t(env)

      flex = env.WhereIs('flex', env['flex_bin'])
      env.Replace(LEX=flex)


   def configure(self, config):
      b = WhereIs("flex", config.conf.env['flex_bin'])

      if not b:
        s = """
        Warning !!! Flex not found !
        Please, install Flex and try again.
        """
        print s
        sys.exit(-1)


def create(config):
   " Create flex tool "
   flex = Flex(config)

   return flex

