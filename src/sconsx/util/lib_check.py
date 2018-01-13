# -- locate executables in the path, use with caution --
def find_executable_path_from_env(exe, strip_bin=True):
    import os
    from os.path import exists, join
    
    paths = os.environ["PATH"].split(os.pathsep)
    okPath = None
    for p in paths:
        if exists(join(p,exe)):
            okPath = p
            break

    if okPath is None : return None
    bin = okPath[-4:]
    if strip_bin and okPath and "bin" in bin and os.sep in bin:
        return okPath[:-4]
    else:
        return okPath


def detect_posix_project_installpath(filepattern, potentialdirs = []):
    """ Detect the installation of include of lib in the system.
        Potential dirs can be added to test on the system.
        By default, '/usr','/usr/local','/opt/local' are tested.
        If nothing is found, it return the default value /usr
        Exemple of use will be:
        detect_posix_project_installpath('GL', ['/usr/X11R6'])
    """
    from os.path import join, exists
    from .env_check import is_conda

    mpotentialdirs = potentialdirs+['/opt/local','/usr/local','/usr']
    if is_conda():
        mpotentialdirs.insert(0,conda_library_prefix())
    for potentialdir in mpotentialdirs:
        if exists(join(potentialdir,filepattern)) :
            return potentialdir
    return '/usr'

