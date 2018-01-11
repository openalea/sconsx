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
""" Readline configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys
from openalea.sconsx.config import *


class Readline:
   def __init__(self, config):
      self.name = 'readline'
      self.config = config
      self._default = {}

   def depends(self):
       return ["termcap"]

   def default(self):
      if CONDA_ENV:
         self._default['include'] = pj(CONDA_LIBRARY_PREFIX, 'include')
         self._default['libpath'] = pj(CONDA_LIBRARY_PREFIX, 'lib')

      elif isinstance(platform, Posix):
           defdir = detect_posix_project_installpath('include/readline/')
           self._default['include'] = join(defdir,'include')
           self._default['libpath']     = join(defdir,'lib') 


   def option( self, opts):

      self.default()

      if isinstance(platform, Posix):
         opts.AddVariables(
            PathVariable('readline_includes',
                        'readline include files',
                        self._default['include']),

            PathVariable(('readline_libpath','readline_lib'),
                        'readline libraries path',
                        self._default['libpath'])
           )


   def update(self, env):
      if isinstance(platform, Posix):
         env.AppendUnique(CPPPATH=[env['readline_includes']])
         env.AppendUnique(LIBPATH=[env['readline_libpath']])
         env.AppendUnique(LIBS=['readline'])


   def configure(self, config):
      if isinstance(platform, Posix):
         if not config.conf.CheckCHeader(['stdio.h',
                                            'string.h',
                                            'readline/readline.h']):
            print("""Error: readline.h not found !!!
            Please install readline and start again.""")
            sys.exit(-1)


def create(config):
   " Create readline tool "
   readline = Readline(config)

   deps= readline.depends()
   for lib in deps:
      config.add_tool(lib)

   return readline

