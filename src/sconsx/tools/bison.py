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
""" Bison configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys, re
from openalea.sconsx.config import *
from os.path import join


def get_bison_version(bisonpath):
    f =os.popen(str(bisonpath)+" --version")
    l =f.readline()
    l =l.split()
    version_text = re.compile(r"\d+.\d+").match(l[-1])
    if version_text is None:
        return None
    version = float(version_text.group(0))
    f.close()
    return version

class Bison:
   def __init__(self, config):
      self.name = 'bison'
      self.config = config
      self._default = {}


   def default(self):

      if CONDA_ENV:
          if os.name == 'posix':
            self._default['bin'] = os.path.join(CONDA_LIBRARY_PREFIX, 'bin')
          else:
            # On windows, the conda package providing bison (m2-bison) is located in Library/usr
            self._default['bin'] = os.path.join(CONDA_LIBRARY_PREFIX, 'usr', 'bin')            
      elif isinstance(platform, Win32):
         try:
            # Try to use openalea egg
            from openalea.deploy import get_base_dir
            base_dir = get_base_dir("bisonflex")
            self._default['bin'] = os.path.join(base_dir, 'bin')
         except:
            self._default['bin'] = r'C:\Tools\Bin'

      elif isinstance(platform, Posix):
         defdir = detect_posix_project_installpath('bin/bison')
         self._default['bin'] = os.path.join(defdir, 'bin')


   def option( self, opts):

      self.default()

      opts.Add('bison_bin', 'Bison binary path',
                self._default['bin'])

      opts.Add(BoolVariable('WITH_BISON',
           'Specify whether you want to compile your project with bison', True))


   def update(self, env):
      """ Update the environment with specific flags """
      import openalea.sconsx.errormsg as em
      if env['WITH_BISON']:
        bison = env.WhereIs('bison', env['bison_bin'])

        if bison:
            version = get_bison_version(bison)
            if version is None:
                em.error("Unable to retrieve bison version number. Problem with bison. Bison disabled ...")
                env['WITH_BISON'] = False
                return

            t = Tool('yacc', toolpath=[getLocalPath()])
            t(env)
            env.Append(YACCFLAGS=['-d', '-v'])
            env.Replace(YACC=bison)

            BISON_HPP = (version >= 1.30)
            env.Append(BISON_HPP=BISON_HPP)

            if BISON_HPP:
               env.Append(CPPDEFINES =["BISON_HPP"])
            env['WITH_BISON'] = True  
            env.Append(CPPDEFINES =["WITH_BISON"])
        else:
          em.error("'bison' not found. Bison disabled ...")
          env['WITH_BISON'] = False  



   def configure(self, config):
      b = WhereIs("bison", config.conf.env['bison_bin'])

      if not b:
        s ="""
        Warning !!! Bison not found !
        Please, install Bison and try again.
        """
        print s
        sys.exit(-1)


def create(config):
   " Create bison tool "
   bison = Bison(config)

   return bison

