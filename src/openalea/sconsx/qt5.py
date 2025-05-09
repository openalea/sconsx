"""SCons.Tool.qt

Tool-specific initialization for Qt.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

#
# Copyright (c) 2001, 2002, 2003, 2004 The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "/home/scons/scons/branch.0/branch.96/baseline/src/engine/SCons/Tool/qt.py 0.96.92.D001 2006/04/10 23:13:27 knight"

import os
import os.path
import re

import SCons.Action
import SCons.Builder
import SCons.Defaults
import SCons.Scanner
import SCons.Tool
import SCons.Util
from SCons.Script.SConscript import SConsEnvironment

#NO_FRAMEWORK = False
class ToolQtWarning(SCons.Warnings.SConsWarning):
    pass

class GeneratedMocFileNotIncluded(ToolQtWarning):
    pass

class QtdirNotFound(ToolQtWarning):
    pass

SCons.Warnings.enableWarningClass(ToolQtWarning)

qrcinclude_re = re.compile(r'<file>([^<]*)</file>', re.M)


header_extensions = [".h", ".hxx", ".hpp", ".hh"]
if SCons.Util.case_sensitive_suffixes('.h', '.H'):
    header_extensions.append('.H')
#cplusplus = __import__('c++', globals(), locals(), [])
#cxx_suffixes = cplusplus.CXXSuffixes
cxx_suffixes = [".c", ".cxx", ".cpp", ".cc"]

def checkMocIncluded(target, source, env):
    moc = target[0]
    cpp = source[0]
    # looks like cpp.includes is cleared before the build stage :-(
    # not really sure about the path transformations (moc.cwd? cpp.cwd?) :-/
    path = SCons.Defaults.CScan.path_function(env, moc.cwd)
    includes = SCons.Defaults.CScan(cpp, env, path)
    if not moc in includes:
        SCons.Warnings.warn(
            GeneratedMocFileNotIncluded,
            "Generated moc file '%s' is not included by '%s'" %
            (str(moc), str(cpp)))

def find_file(filename, paths, node_factory):
    retval = None
    for udir in paths:
        node = node_factory(filename, udir)
        if node.rexists():
            return node
    return None

class _Automoc:
    """
    Callable class, which works as an emitter for Programs, SharedLibraries and
    StaticLibraries.
    """

    def __init__(self, objBuilderName):
        self.objBuilderName = objBuilderName

    def __call__(self, target, source, env):
        """
        Smart autoscan function. Gets the list of objects for the Program
        or Lib. Adds objects and builders for the special qt files.
        """
        try:
            if int(env.subst('$QT5_AUTOSCAN')) == 0:
                return target, source
        except ValueError:
            pass
        try:
            debug = int(env.subst('$QT5_DEBUG'))
        except ValueError:
            debug = 0

        # some shortcuts used in the scanner
        _FS = SCons.Node.FS.default_fs
        splitext = SCons.Util.splitext
        objBuilder = getattr(env, self.objBuilderName)

        # some regular expressions:
        # Q_OBJECT detection
        q_object_search = re.compile(r'[^A-Za-z0-9]Q_OBJECT[^A-Za-z0-9]')
        # cxx and c comment 'eater'
        #comment = re.compile(r'(//.*)|(/\*(([^*])|(\*[^/]))*\*/)')
        # CW: something must be wrong with the regexp. See also bug #998222
        #     CURRENTLY THERE IS NO TEST CASE FOR THAT

        # The following is kind of hacky to get builders working properly(FIXME)
        objBuilderEnv = objBuilder.env
        objBuilder.env = env
        mocBuilderEnv = env.Moc5.env
        env.Moc5.env = env

        # make a deep copy for the result; MocH objects will be appended
        out_sources = source[:]

        for obj in source:
            if not obj.has_builder():
                # binary obj file provided
                if debug:
                    print("scons: qt: '%s' seems to be a binary. Discarded." \
                        % str(obj))
                continue
            try:
                cpp = obj.sources[0]
            except:
                continue
            if not splitext(str(cpp))[1] in cxx_suffixes:
                if debug:
                    print("scons: qt: '%s' is no cxx file. Discarded." \
                        % str(cpp))
                # c or fortran source
                continue
            #cpp_contents = comment.sub('', cpp.get_contents())
            try:
                cpp_contents = cpp.get_contents()
            except:
                continue # may be an still not generated source
            h = None
            for h_ext in header_extensions:
                # try to find the header file in the corresponding source
                # directory
                hname = splitext(cpp.name)[0] + h_ext
                h = find_file(hname, (cpp.get_dir(),), env.File)
                if h:
                    if debug:
                        print("scons: qt: Scanning '%s' (header of '%s')" % \
                            (str(h), str(cpp)))
                    #h_contents = comment.sub('', h.get_contents())
                    h_contents = h.get_contents()
                    break
            if not h and debug:
                print("scons: qt: no header for '%s'." % (str(cpp)))
            if h and q_object_search.search(h_contents):
                # h file with the Q_OBJECT macro found -> add moc_cpp
                moc_cpp = env.Moc5(h)
                moc_o = objBuilder(moc_cpp)
                out_sources.append(moc_o)
                #moc_cpp.target_scanner = SCons.Defaults.CScan
                if debug:
                    print("scons: qt: found Q_OBJECT macro in '%s', moc'ing to '%s'" % (str(h), str(moc_cpp)))
            if cpp and q_object_search.search(cpp_contents):
                # cpp file with Q_OBJECT macro found -> add moc
                # (to be included in cpp)
                moc = env.Moc5(cpp)
                env.Ignore(moc, moc)
                if debug:
                    print("scons: qt: found Q_OBJECT macro in '%s', moc'ing to '%s'" % (str(cpp), str(moc)))
                #moc.source_scanner = SCons.Defaults.CScan
        # restore the original env attributes (FIXME)
        objBuilder.env = objBuilderEnv
        env.Moc5.env = mocBuilderEnv

        return (target, out_sources)

AutomocShared = _Automoc('SharedObject')
AutomocStatic = _Automoc('StaticObject')

def _detect(env):
    """Not really safe, but fast method to detect the QT library"""

    QTDIR = env.get('QTDIR', None)
    if QTDIR!=None:
        return QTDIR

    QTDIR = os.environ.get('QTDIR',None)
    if QTDIR!=None:
        return QTDIR

    moc = env.WhereIs('moc-qt5') or env.WhereIs('moc5') or env.WhereIs('moc')
    if moc:
        SCons.Warnings.warn(
            QtdirNotFound,
            "QTDIR variable is not defined, using moc executable as a hint (QTDIR=%s)" % QTDIR)
        return os.path.dirname(os.path.dirname(moc))

    SCons.Warnings.warn(
        QtdirNotFound,
        "Could not detect qt, using empty QTDIR")
    return None

def generate(env):
    """Add Builders and construction variables for qt to an Environment."""

    print("Loading qt5 tool...")

    def locateQt5Command(env, command, qtdir) :
        fullpath1 = os.path.join(qtdir, 'bin', command +'-qt5')
        if (os.access(fullpath1, os.X_OK) or
            os.access(fullpath1+".exe", os.X_OK)):
            return fullpath1
        fullpath3 = os.path.join(qtdir, 'bin', command +'5')
        if (os.access(fullpath3, os.X_OK) or
            os.access(fullpath3+".exe", os.X_OK)):
            return fullpath3
        fullpath2 = os.path.join(qtdir, 'bin', command)
        if (os.access(fullpath2, os.X_OK) or
            os.access(fullpath2+".exe", os.X_OK)):
            return fullpath2
        fullpath = env.Detect([command+'-qt5', command+'5', command])
        if not (fullpath is None):
            return fullpath
        raise Exception("Qt4 command '" + command + "' not found. Tried: " + fullpath1 + " and "+ fullpath2)


    CLVar = SCons.Util.CLVar
    Action = SCons.Action.Action
    Builder = SCons.Builder.Builder
    splitext = SCons.Util.splitext

    env['QTDIR']  = _detect(env)
    # TODO: 'Replace' should be 'SetDefault'
#    env.SetDefault(
    env.Replace(
        QTDIR  = _detect(env),
        QT5_BINPATH = os.path.join('$QTDIR', 'bin'),
        QT5_CPPPATH = os.path.join('$QTDIR', 'include'),
        QT5_LIBPATH = os.path.join('$QTDIR', 'lib'),
        # TODO: This is not reliable to QTDIR value changes but needed in order to support '-qt4' variants
        QT5_MOC = locateQt5Command(env,'moc', env['QTDIR']),
        QT5_UIC = locateQt5Command(env,'uic', env['QTDIR']),
        QT5_RCC = locateQt5Command(env,'rcc', env['QTDIR']),
        QT5_LUPDATE = locateQt5Command(env,'lupdate', env['QTDIR']),
        QT5_LRELEASE = locateQt5Command(env,'lrelease', env['QTDIR']),
        QT5_LIB = '', # KLUDGE to avoid linking qt3 library

        QT5_AUTOSCAN = 1, # Should the qt tool try to figure out, which sources are to be moc'ed?

        # Some QT specific flags. I don't expect someone wants to
        # manipulate those ...
        QT5_UICFLAGS = CLVar(''),
        QT5_MOCFROMHFLAGS = CLVar(''),
        QT5_MOCFROMCXXFLAGS = CLVar('-i'),
        QT5_QRCFLAGS = '',

        # suffixes/prefixes for the headers / sources to generate
        QT5_UISUFFIX = '.ui',
        QT5_UICDECLPREFIX = 'ui_',
        QT5_UICDECLSUFFIX = '.h',
        QT5_MOCHPREFIX = 'moc_',
        QT5_MOCHSUFFIX = '$CXXFILESUFFIX',
        QT5_MOCCXXPREFIX = 'moc_',
        QT5_MOCCXXSUFFIX = '.moc',
        QT5_QRCSUFFIX = '.qrc',
        QT5_QRCCXXSUFFIX = '$CXXFILESUFFIX',
        QT5_QRCCXXPREFIX = 'qrc_',

        # Commands for the qt support ...
        QT5_UICCOM = '$QT5_UIC $QT5_UICFLAGS -o $TARGET $SOURCE',
        QT5_MOCFROMHCOM = '$QT5_MOC $QT5_MOCFROMHFLAGS -o $TARGET $SOURCE',
        QT5_MOCFROMCXXCOM = [
            '$QT5_MOC $QT5_MOCFROMCXXFLAGS -o $TARGET $SOURCE',
            Action(checkMocIncluded,None)],
        QT5_LUPDATECOM = '$QT5_LUPDATE $SOURCE -ts $TARGET',
        QT5_LRELEASECOM = '$QT5_LRELEASE $SOURCE',
        QT5_RCCCOM = '$QT5_RCC $QT5_QRCFLAGS $SOURCE -o $TARGET',
        )

    # Translation builder
    tsbuilder = Builder(
        action = SCons.Action.Action('$QT5_LUPDATECOM'), #,'$QT5_LUPDATECOMSTR'),
        multi=1
        )
    env.Append( BUILDERS = { 'Ts': tsbuilder } )
    qmbuilder = Builder(
        action = SCons.Action.Action('$QT5_LRELEASECOM'),# , '$QT5_LRELEASECOMSTR'),
        src_suffix = '.ts',
        suffix = '.qm',
        single_source = True
        )
    env.Append( BUILDERS = { 'Qm': qmbuilder } )

    # Resource builder
    def scanResources(node, env, path, arg):
        contents = node.get_contents()
        includes = qrcinclude_re.findall(contents)
        return includes
    qrcscanner = SCons.Scanner.Scanner(name = 'qrcfile',
        function = scanResources,
        argument = None,
        skeys = ['.qrc'])
    qrcbuilder = Builder(
        action = SCons.Action.Action('$QT5_RCCCOM'), #, '$QT5_RCCCOMSTR'),
        source_scanner = qrcscanner,
        src_suffix = '$QT5_QRCSUFFIX',
        suffix = '$QT5_QRCCXXSUFFIX',
        prefix = '$QT5_QRCCXXPREFIX',
        single_source = True
        )
    env.Append( BUILDERS = { 'Qrc': qrcbuilder } )

    # Interface builder
    uic5builder = Builder(
        action = SCons.Action.Action('$QT5_UICCOM'), #, '$QT5_UICCOMSTR'),
        src_suffix='$QT5_UISUFFIX',
        suffix='$QT5_UICDECLSUFFIX',
        prefix='$QT5_UICDECLPREFIX',
        single_source = True
        #TODO: Consider the uiscanner on new scons version
        )
    env.Append( BUILDERS = { 'Uic5': uic5builder } )

    # Metaobject builder
    mocBld = Builder(action={}, prefix={}, suffix={})
    for h in header_extensions:
        act = SCons.Action.Action('$QT5_MOCFROMHCOM') #, '$QT5_MOCFROMHCOMSTR')
        mocBld.add_action(h, act)
        mocBld.prefix[h] = '$QT5_MOCHPREFIX'
        mocBld.suffix[h] = '$QT5_MOCHSUFFIX'
    for cxx in cxx_suffixes:
        act = SCons.Action.Action('$QT5_MOCFROMCXXCOM') #, '$QT5_MOCFROMCXXCOMSTR')
        mocBld.add_action(cxx, act)
        mocBld.prefix[cxx] = '$QT5_MOCCXXPREFIX'
        mocBld.suffix[cxx] = '$QT5_MOCCXXSUFFIX'
    env.Append( BUILDERS = { 'Moc5': mocBld } )

    # er... no idea what that was for
    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)
    static_obj.src_builder.append('Uic5')
    shared_obj.src_builder.append('Uic5')

    # We use the emitters of Program / StaticLibrary / SharedLibrary
    # to scan for moc'able files
    # We can't refer to the builders directly, we have to fetch them
    # as Environment attributes because that sets them up to be called
    # correctly later by our emitter.
    env.AppendUnique(PROGEMITTER =[AutomocStatic],
                     SHLIBEMITTER=[AutomocShared],
                     LIBEMITTER  =[AutomocStatic],
                     # Of course, we need to link against the qt libraries
                     CPPPATH=["$QT5_CPPPATH"],
                     LIBPATH=["$QT5_LIBPATH"],
                     LIBS=['$QT5_LIB'])

    #import new
    #method = new.instancemethod(enable_modules, env, SCons.Environment)
    #env.EnableQt4Modules=method
    SConsEnvironment.EnableQt5Modules = enable_modules
    SConsEnvironment.EnableQtModules = enable_modules


def enable_modules(self, modules, debug=False, suffix = '') :
    import sys

    validModules = [
        # Qt Essentials
        'QtCore',
        'QtGui',
        'QtMultimedia',
        'QtMultimediaQuick_p',
        'QtMultimediaWidgets',
        'QtNetwork',
        'QtPlatformSupport',
        'QtQml',
        'QtQmlDevTools',
        'QtQuick',
        'QtQuickParticles',
        'QtSql',
        'QtQuickTest',
        'QtTest',
        'QtWebKit',
        'QtWebKitWidgets',
        'QtWidgets',
        # Qt Add-Ons
        'QtConcurrent',
        'QtDBus',
        'QtOpenGL',
        'QtPrintSupport',
        'QtDeclarative',
        'QtScript',
        'QtScriptTools',
        'QtSvg',
        'QtUiTools',
        'QtXml',
        'QtXmlPatterns',
        # Qt Tools
        'QtHelp',
        'QtDesigner',
        'QtDesignerComponents',
        # Other
        'QtCLucene',
        'QtConcurrent',
        'QtV8'
        ]
    pclessModules = [
    ]
    staticModules = [
    ]
    invalidModules=[]
    for module in modules:
        if module not in validModules :
            invalidModules.append(module)
    if invalidModules :
        raise Exception("Modules %s are not Qt5 modules. Valid Qt5 modules are: %s"% (
            str(invalidModules),str(validModules)))

    moduleDefines = {
        'QtScript'   : ['QT_SCRIPT_LIB'],
        'QtSvg'      : ['QT_SVG_LIB'],
        'QtSql'      : ['QT_SQL_LIB'],
        'QtXml'      : ['QT_XML_LIB'],
        'QtOpenGL'   : ['QT_OPENGL_LIB'],
        'QtGui'      : ['QT_GUI_LIB'],
        'QtNetwork'  : ['QT_NETWORK_LIB'],
        'QtCore'     : ['QT_CORE_LIB'],
        'QtWidgets'  : ['QT_WIDGETS_LIB'],
    }
    for module in modules :
        try : self.AppendUnique(CPPDEFINES=moduleDefines[module])
        except: pass
    debugSuffix = ''
    if sys.platform == "linux2" :
        if debug : debugSuffix = '_debug'

        PKG_CONFIG_PATH = os.environ.get('PKG_CONFIG_PATH')
        if PKG_CONFIG_PATH:
            self['ENV']['PKG_CONFIG_PATH'] = PKG_CONFIG_PATH
        self.AppendUnique(LIBPATH=["$QT5_LIBPATH"])
        qt5_inc = self.subst('$QT5_CPPPATH')
        for qt_ext in ("qt5", "qt"):
            if os.path.exists(os.path.join(qt5_inc, qt_ext)):
                self.AppendUnique(CPPPATH=[os.path.join("$QT5_CPPPATH", qt_ext)])
                for module in modules :
                    if module not in pclessModules:
                        continue
                    self.AppendUnique(LIBS=[module+debugSuffix]) # TODO: Add the debug suffix
                    self.AppendUnique(CPPPATH=[os.path.join("$QT5_CPPPATH", qt_ext, module)])
                    break
        else:
            #self.AppendUnique(CPPPATH=["$QT5_CPPPATH"])
            for module in modules :
                if module not in pclessModules:
                    continue
                self.AppendUnique(LIBS=[module+debugSuffix]) # TODO: Add the debug suffix
                self.AppendUnique(CPPPATH=[os.path.join("$QT5_CPPPATH",module)])
        pcmodules = [module+debugSuffix for module in modules if module not in pclessModules]
        try:
            self.ParseConfig('pkg-config %s --libs --cflags'% ' '.join(pcmodules))
        except:
            pass
        return

    if sys.platform == "win32" :
        if debug : debugSuffix = 'd'
        self.AppendUnique(LIBS=[lib.replace('Qt','Qt5')+debugSuffix for lib in modules if lib not in staticModules])
        self.AppendUnique(LIBS=[lib+debugSuffix for lib in modules if lib in staticModules])
        if 'QtOpenGL' in modules:
            self.AppendUnique(LIBS=['opengl32','glu32'])
        qt5_inc = self.subst('$QT5_CPPPATH')
        for qt_ext in ("qt5", "qt"):
            if os.path.exists(os.path.join(qt5_inc, qt_ext)):
                self.AppendUnique(CPPPATH=[os.path.join("$QT5_CPPPATH", qt_ext)])
                for module in modules :
                    self.AppendUnique(CPPPATH=[os.path.join("$QT5_CPPPATH", qt_ext, module)])
                break
        else:
            self.AppendUnique(CPPPATH=[ '$QTDIR/include/'+module for module in modules])
        self.AppendUnique(LIBPATH=[os.path.join('$QTDIR','lib')])
        return

    if sys.platform == "darwin" :
        if not suffix:
            suffix = '.5'

        QT_FRAMEWORK = self['QT5_FRAMEWORK']

        # TODO: Test debug version on Mac
        self.AppendUnique(LIBPATH=["$QT5_LIBPATH"])
        if QT_FRAMEWORK:
            self.AppendUnique(CXXFLAGS="-F$QTDIR/lib")
            self.AppendUnique(LINKFLAGS="-F$QTDIR/lib")
            self.AppendUnique(LINKFLAGS="-F$QTDIR/Library/Frameworks") # To check by @CP
            self.AppendUnique(LINKFLAGS="-L$QTDIR/lib") #TODO clean!
        if debug : debugSuffix = 'd'
        if suffix : debugSuffix = '.5'

        self.AppendUnique(CPPPATH=["$QT5_CPPPATH"])
        for module in modules :
            self.AppendUnique(CPPPATH=[os.path.join("$QT5_CPPPATH",module)])

            if not QT_FRAMEWORK:
                self.AppendUnique(LIBS=[module+debugSuffix]) # TODO: Add the debug suffix
                #self.AppendUnique(LIBPATH=[os.path.join("$QTDIR","lib")])
            else:
                if module in pclessModules :
                    self.AppendUnique(LIBS=[module+debugSuffix]) # TODO: Add the debug suffix
                    self.AppendUnique(LIBPATH=[os.path.join("$QTDIR","lib")])
                else :
                    self.Append(LINKFLAGS=['-framework', module])
        if 'QtOpenGL' in modules:
            self.AppendUnique(LINKFLAGS="-F/System/Library/Frameworks")
            self.Append(LINKFLAGS=['-framework', 'AGL']) #TODO ughly kludge to avoid quotes
            self.Append(LINKFLAGS=['-framework', 'OpenGL'])
        return
# This should work for mac but doesn't
#    env.AppendUnique(FRAMEWORKPATH=[os.path.join(env['QTDIR'],'lib')])
#    env.AppendUnique(FRAMEWORKS=['QtCore','QtGui','QtOpenGL', 'AGL'])


def exists(env):
    return True
        #return _detect(env)


