
def detect_qt_includepath():
    from .lib_check import detect_posix_project_installpath, find_executable_path_from_env
    import os
    from os.path import join, abspath

    defaultdirs = ['/opt/local/libexec']
    qt_dir = os.getenv("QTDIR")
    if qt_dir : defaultdirs.append(qt_dir)
    qt_dir = find_executable_path_from_env("moc.exe", strip_bin=True)
    if qt_dir : defaultdirs.append(abspath(join(qt_dir,os.pardir)))

    for pattern in ['qt4/include','qt5/include','qt/include','include/qt4','include/qt5','include/qt']:
        defdir = os.path.join(detect_posix_project_installpath(join(pattern,'QtCore'),defaultdirs),pattern)
        if os.path.exists(defdir):
            break
    return defdir


def detect_installed_qt_version(default = 4):
    import os
    from .versionreader import read_variable, version_from_hex

    QT_VERSION = None
    library_inc = detect_qt_includepath()

    qversionconfig = os.path.join(library_inc,'QtCore','qconfig.h')
    if os.path.exists(qversionconfig):
        variable = 'QT_VERSION_MAJOR'
        QT_VERSION = read_variable(variable, qversionconfig)
    if QT_VERSION is None:
        qversionconfig = os.path.join(library_inc,'QtCore','qglobal.h')
        if os.path.exists(qversionconfig):
            variable = 'QT_VERSION'
            QT_VERSION = read_variable(variable, qversionconfig)
        if QT_VERSION is None:
            print ('Autodetect qt error in',repr(library_inc))
            QT_VERSION = default

    return QT_VERSION

