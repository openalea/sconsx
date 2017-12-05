# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2016 CIRAD - INRIA - INRA
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

import os
from openalea.sconsx.config import *


class BuildDir:
    """Define Variant Dir options for putting build files outside the source tree."""

    def __init__(self, config):
        """Pluggin definition."""
        self.name = 'build_dir'
        self.config = config
        self._default = {}

    def default(self):
        """Set the default directory values for build_prefix."""
        # self._default['build_prefix']= pj(self.config.dir[0], "build-" + platform.name)
        #if 'CONDA_BUILD' in os.environ:
        #    self._conda_build = True
        #    prefix = self._default['build_prefix'] = CONDA_LIBRARYPREFIX
        #else:
        #    self._conda_build = False
        #    prefix = self._default['build_prefix'] = pj(self.config.dir[0],"build-scons")

        prefix = self._default['build_prefix'] = pj(self.config.dir[0],"build-scons")
        self._conda_build = ('CONDA_BUILD' in os.environ)


        self._default['build_bindir'] = pj(prefix,"bin")
        self._default['build_libdir'] = pj(prefix,"lib")
        self._default['build_includedir'] = pj(prefix,"include")

    def option(self, opts):
        """Define user options to redefine the default values."""
        self.default()
        opts.Add(BoolVariable('with_build_dir', 'build files in a separate directory?', True))
        opts.Add('build_prefix',
                 'local preinstall directory',
                 self._default['build_prefix'])
        opts.Add('build_bindir',
                 'local preinstall directory for binaries',
                 self._default['build_bindir'])
        opts.Add('build_libdir',
                 'local preinstall directory for libraries',
                 self._default['build_libdir'])
        opts.Add('build_includedir',
                 'local preinstall directory for headers',
                 self._default['build_includedir'])

    def update(self, env):
        """Update the environment with specific flags."""
        if env['with_build_dir'] or self._conda_build:
            prefix = env['build_prefix']
            bin_prefix = env['build_bindir']
            lib_prefix = env['build_libdir']
            inc_prefix = env['build_includedir']
        else:
            prefix = self.config.dir[0]
            bin_prefix = pj(prefix, 'bin')
            lib_prefix = pj(prefix, 'lib')
            inc_prefix = pj(prefix, 'include')

        build = {
            'build_prefix': prefix,
            'build_bindir': bin_prefix,
            'build_libdir': lib_prefix,
            'build_includedir': inc_prefix}

        if env['with_build_dir']:
            build['build_dir'] = pj(prefix, 'src')

        # Creation of missing directories
        for udir in build:
            _path = build[udir]
            env[udir] = os.path.abspath(_path)
            if _path and not os.path.exists(_path):
                os.makedirs(_path)

        if not env['with_build_dir']:
            env['build_dir'] = pj(env['build_prefix'], 'src')

    def configure(self, config):
        """Configure code needs to go here."""
        pass


def create(config):
    """Create builddir tool."""
    builddir = BuildDir(config)

    return builddir
