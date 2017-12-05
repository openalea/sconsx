# -*-python-*-
#-------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#-------------------------------------------------------------------------
""" Eigen configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"


import os
import sys
from openalea.sconsx.config import *


class Eigen:

    def __init__(self, config):
        self.name = 'eigen'
        self.config = config
        self._default = {}

    def default(self):
        name = str(platform)
        if CONDA_ENV:
            inc_path = pj(CONDA_LIBRARYPREFIX, 'include', 'eigen3')
        elif isinstance(platform, Linux):
            dist = platform.distribution()
            name += " " + dist
            if dist == "ubuntu":
                inc_path = "/usr/include/eigen2/"
            else:
                inc_path = "/usr/include/"
        elif isinstance(platform, Win32):
            try:
                import openalea.config as conf
                inc_path = conf.include_dir
            except ImportError as e:
                inc_path = 'C:' + os.sep
        elif isinstance(platform, Darwin):
            inc_path = '/opt/local/include/eigen3'

        self._default['include'] = inc_path

    def option(self, opts):
        self.default()
        opts.AddVariables(
            ('eigen_includes',
             'eigen include files',
             self._default['include']),
            BoolVariable(
                'WITH_EIGEN',
                'Specify whether you want to compile your project with EIGEN',
                True))

    def update(self, env):
        """ Update the environment with specific flags """
        if env['WITH_EIGEN']:
            eigen_includes = env['eigen_includes']
            if isinstance(eigen_includes, str):
                eigen_includes = eigen_includes.split()
            eigen_includes = eigen_includes[0]
            if not os.path.exists(os.path.join(eigen_includes, 'Eigen')):
                import warnings
                warnings.warn("Error: EIGEN lib not found. EIGEN disabled ...")
                env['WITH_EIGEN'] = False
        if env['WITH_EIGEN']:
            env.AppendUnique(CPPPATH=[env['eigen_includes']])
            env.Append(CPPDEFINES='WITH_EIGEN')

    def configure(self, config):
        if not config.conf.CheckCHeader('Eigen/Core'):
            print """Error: Eigen headers not found !!!
         Please install eigen and start again."""
            sys.exit(-1)


def create(config):
    " Create eigen tool "
    eigen = Eigen(config)

    return eigen
