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
""" Pthread configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"


import os, sys
from openalea.sconsx.config import *

pj = os.path.join

class Pthread:
   def __init__(self, config):
      self.name = 'pthread'
      self.config = config
      self._default = {}


   def default(self):
      if CONDA_ENV:
         prefix = CONDA_PREFIX
      else:
         prefix = detect_posix_project_installpath('include/pthread.h')

      self._default['include'] = pj(prefix, 'include')
      self._default['libpath'] = pj(prefix, 'lib')



   def option( self, opts):

      self.default()

      opts.AddVariables(
         PathVariable('pthread_includes', 'pthread include files',
                     self._default['include']),
         PathVariable(('pthread_libpath','pthread_lib'), 'pthread libraries path',
                     self._default['libpath'])
     )



   def update(self, env):
      """ Update the environment with specific flags """

      env.AppendUnique(CPPPATH=[env['pthread_includes']])
      env.AppendUnique(LIBPATH=[env['pthread_libpath']])
      env.AppendUnique(LIBS=['pthread'])



   def configure(self, config):
      if not config.conf.CheckCHeader('pthread.h'):
         print """Error: pthread.h not found !!!
         Please install pthread and start again."""
         sys.exit(-1)


def create(config):
   " Create pthread tool "
   pthread = Pthread(config)

   return pthread

