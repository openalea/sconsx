SconsX provides a set of tools with default options, configurations  and dependencies.

Each tool provides:
  * A set of options with default values dependeing on the OS.
  * A list of dependecies. For instance, Boost.Python depends on Python.
  * A configuration method that use **SConf**, the configuartion tool used by **SCons**.
  * An update method that update the SCons environment with specific flags.

Available tools are limited but can be easily extended :
  * **compiler**: Define a set of generic flags (e.g. debug or warning) for compilers on various OS.
  * **builddir**: Define a build directory for build objects and sub directories for header files, lib and bin files created during the build.
  * **install**:  Define install directories used during the install stage, i.e. exec and exec_prefix, libdir, bindir and includedir as well as datadir.
  * Other tools: **OpenGL**, **QT**, **bison**, **flex**, **Boost.Python**, ...