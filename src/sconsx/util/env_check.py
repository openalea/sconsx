#------------------------------------------------------------------------------
# Conda detection
import os


def is_conda():
    """ Check if sconsx is run in a conda environment. """
    return ("CONDA_PREFIX" in os.environ)

def conda_prefix():
    """ Returns the PREFIX where lib, include are installed. """
    if is_conda():
        if 'CONDA_BUILD' in os.environ:
            return os.environ.get('PREFIX', os.environ.get('CONDA_PREFIX'))
        else:
            return os.environ['CONDA_PREFIX']

def conda_library_prefix():
    if os.name == 'posix' : 
        return conda_prefix()
    elif is_conda():
        library_prefix= os.path.join(os.environ.get('CONDA_PREFIX'),'Library')
        if 'CONDA_BUILD' in os.environ:
            return os.environ.get('LIBRARY_PREFIX', library_prefix)
        else:
            return library_prefix
#------------------------------------------------------------------------------
# system detection

def is_32bit_environment():
    return not is_64bit_environment()

def is_64bit_environment():
    import sys
    return sys.maxsize.bit_length() == 63

#------------------------------------------------------------------------------
# CI detection

def is_continuous_integration():
    import os
    return 'CI' in os.environ

def is_on_travis():
    import os
    return 'TRAVIS' in os.environ

def is_on_appveyor():
    import os
    return 'APPVEYOR' in os.environ    