[![License: GPL](https://img.shields.io/badge/License-GPL-blue.svg)](https://opensource.org/licenses/GPL-3.0)
[![CI status](https://github.com/openalea/sconsx/actions/workflows/conda-package-build.yml/badge.svg)](https://github.com/openalea/sconsx/actions/workflows/conda-package-build.yml)
[![Documentation Status](https://readthedocs.org/projects/sconsx/badge/?version=latest)](https://sconsx.readthedocs.io/en/latest/?badge=latest)


# SConsX

SConsX is a package of the OpenAlea project.

## About

**SConsX** is an extension package of the famous [SCons](http://www.scons.org) build tool.  
SConsX aims to simplify the build of complex multi-platform packages (i.e. using C++, Boost.Python and Python).

Like **Boost.Jam** or **qmake**, it knows about different types of compilers, and the different steps involved in compiling for Windows and Linux.  
This knowledge allows the user to describe what needs to be built in high-level terms, without concern for low-level details such as the compiler's specific flags or how the operating system handles dynamic libraries.

The goal is to write a single, simple build description (`SConstruct` and `SConscript`) that is likely to work for several compilers on Linux and Windows.  
It also has built-in support for variant builds (e.g. debug, release), options (e.g. include paths and threading options), and dependencies associated with specific libraries.  
The build objects are created in a separate build directory, not in the source directory.

**SConsX** extends **SCons** by adding knowledge to existing system-dependent tools (e.g. default options and paths, tool dependencies).  
All internal options can be overridden in an external configuration file (named `option.py`).  
For each tool, **SConsX** also adds configuration capabilities that mimic autoconf functionalities.

**SConsX** is just a thin wrapper over SCons. It is easily
extendible. You can add new tools as well as new high-level commands.

**SConsX** is under development. Lot of work have to be done for a better support of new compiler (e.g. Visual C++, mingw), new tools and new functionalities.

## Description

SConsX provides a set of tools with default options, configurations, and dependencies.

Each tool provides:

- A set of options with default values depending on the OS.
- A list of dependencies (e.g. Boost.Python depends on Python).
- A configuration method that uses **SConf**, the configuration tool used by **SCons**.
- An update method that updates the SCons environment with specific flags.

Available tools are limited but can be easily extended:

- **compiler**: Defines generic flags (e.g. debug or warning) for compilers across various OSes.
- **builddir**: Defines a build directory for object files and subdirectories for headers, libs, and binaries created during the build.
- **install**: Defines installation directories used during the install stage, such as `exec`, `exec_prefix`, `libdir`, `bindir`, `includedir`, and `datadir`.
- Other tools: **OpenGL**, **QT**, **bison**, **flex**, **Boost.Python**, ...

## Quick Example

This is a `SConstruct` file.  
See the [SCons documentation](http://www.scons.org) for more information.

```python
import sconsx
from sconsx import config

# Creation of a SCons object
# Set an option file as well as command line args.
option = Options("options.py", ARGUMENTS)

# Creation of a SConsX object 
conf = config.Config(['install', 'boost.python', 'qt'])

# Update the SCons option with the default settings of each tool
conf.UpdateOptions(option)

# Creation of the SCons Environment
env = Environment(options=option)

# Update the environment with specific flags defined by SConsX and the user
conf.Update(env)

SConscript(...)
```

## Installation

### Download

SConsX is available on github.

#### Requirements

There are two requirements:
  * SCons (http://www.scons.org) version >= 4.
  * setuptools

#### Installation

```bash
mamba install -c openalea3 -c conda-forge openalea.sconsx
```

For developers

```bash
git clone https://github.com/openalea/sconsx
cd sconsx
pip install -e .
```

