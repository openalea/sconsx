# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------

__doc__=""" OpenAlea configure environment. """
__license__= "Cecill-C"
__revision__="$Id: alea.py 593 2007-06-20 08:04:14Z pradal $"

import os, sys
from openalea.sconsx.config import *


class EggLib:

   def __init__(self, name, config):
      
      self.name = name
      self.config = config
      self._default = {}

      self.lib_key = = "%s_lib"%(self.name)
      self.include_key = = "%s_include"%(self.name)
      
      
      
   def default( self ):
      """Set default tool values"""


      try:
         from openalea.deploy import get_include_dirs, get_lib_dirs
      
         self._default[self.lib_key] = get_lib_dirs(self.name)
         self._default[self.include_key] = get_include_dirs(self.name)

      except:
         
         self._default[self.lib_key] = ""
         self._default[self.include_key] = ""
      

   def option(  self, opts ):
      """Add scons options to opts"""
      
      self.default()

      opts.Add( self.lib_key,
                self.lib_key + ' directory', 
                self._default[self.lib_key] )
      
      opts.Add( self.include_key,
                self.include_key + ' directory', 
                self._default[self.include_key])


   def update( self, env ):
      """ Update the environment with specific flags """

      env.AppendUnique( CPPPATH=[env[self.include_key]] )
      env.AppendUnique( LIBPATH=[env[self.lib_key]] )

      #env.EnableALEALib= _EnableALEALib

   def configure( self, config ):
      pass


