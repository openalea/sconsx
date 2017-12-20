# -*-python-*-
#--------------------------------------------------------------------------------
#
#        OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Frederic Boudon <frederic.boudon@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------
""" Boost.Python configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys
from openalea.sconsx.config import *
from boost_base import BoostBase

ModuleInterDependency = {
    
}

ModuleDefines = {
    'python' :'BOOST_PYTHON_DYNAMIC_LIB'
}

ModuleFlags = {
    'python' :' -ftemplate-depth-100 ' if isinstance(platform, Posix) else '',
    'thread' :' -ftemplate-depth-100 ' if isinstance(platform, Posix) else ''
}


def EnableBoostModule(env, libname):
    libfullname= 'boost_' + libname + env['boost_libs_suffix']
    env.AppendUnique(LIBS=[libfullname])
    if libname in ModuleDefines:
        env.Append(CPPDEFINES=ModuleDefines[libname])
    if libname in ModuleFlags:
        env.Append(CPPFLAGS=ModuleFlags[libname])
    if libname in ModuleInterDependency:
        for boostmodule in ModuleInterDependency[libname]:
            EnableBoostModule(env, boostmodule)


class Boost(BoostBase):

    def update(self, env):
        """ Update the environment with specific flags """
        if env['WITH_BOOST']:
            env.AppendUnique(CPPPATH=[env['boost_includes']])
            env.AppendUnique(LIBPATH=[env['boost_libpath']])
            env.EnableBoostModule = EnableBoostModule


def create(config):
    " Create boost tool "
    boost = Boost(config)

    deps= boost.depends()
    for lib in deps:
        config.add_tool(lib)

    return boost
