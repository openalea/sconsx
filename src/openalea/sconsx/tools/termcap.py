# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2016 INRIA - CIRAD - INRA
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
""" Termcap configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys
from openalea.sconsx.config import *


class Termcap:
   def __init__(self, config):
      self.name = 'termcap'
      self.config = config
      self._default = {}


   def default(self):
      self._default['ncurses'] = False
      if CONDA_ENV:
         self._default['include'] = pj(CONDA_LIBRARY_PREFIX, 'include')
         self._default['libpath'] = pj(CONDA_LIBRARY_PREFIX, 'lib')
      elif isinstance(platform, Posix):
            defdir = detect_posix_project_installpath('include/termcap.h')
            self._default['include'] = join(defdir,'include')
            self._default['libpath']     = join(defdir,'lib')
            self._default['ncurses'] = False


   def option( self, opts):
      if isinstance(platform, Posix):
         self.default()

         opts.AddVariables(
            PathVariable('termcap_includes', 'termcap include files',
                        self._default['include']),
            PathVariable(('termcap_libpath','termcap_lib'), 'termcap libraries path',
                        self._default['libpath'])

           )
         opts.Add(BoolVariable('WITH_NCURSES', 'Use ncurses instead of termcap',
                 self._default['ncurses']))


   def update(self, env):
      if isinstance(platform, Posix):
         env.AppendUnique(CPPPATH=[env['termcap_includes']])
         env.AppendUnique(LIBPATH=[env['termcap_libpath']])
         termcap_lib = 'termcap'
         if env['WITH_NCURSES']:
            termcap_lib = 'ncurses'
         env.AppendUnique(LIBS=[termcap_lib])


   def configure(self, config):
      if isinstance(platform, Posix):
         if not config.conf.CheckCHeader('termcap.h'):
            print("""Error: termcap.h not found !!!
            Please install termcap and start again.""")
            sys.exit(-1)


def create(config):
   " Create termcap tool "
   termcap = Termcap(config)

   return termcap

