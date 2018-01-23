
import os
import sys

#------------------------------------------------------------------------------
# Conda detection

def is_conda():
    """ Check if sconsx is run in a conda environment. """
    return ("CONDA_PREFIX" in os.environ)

def is_conda_build():
    """ Check if sconsx is run in a conda environment. """
    return ("CONDA_BULD" in os.environ)

def conda_prefix():
    """ Returns the PREFIX where conda environement is installed. """
    if is_conda():
        
        prefix= os.environ.get('CONDA_PREFIX')
        if is_conda_build():
            prefix = os.environ.get('PREFIX', prefix)

        return prefix

def conda_library_prefix():
    """ Returns the PREFIX where lib, include are installed. """
    if is_conda():
        
        library_prefix = conda_prefix()
        if os.name == 'nt' : 
            library_prefix = os.path.join(library_prefix,'Library')

        if is_conda_build():
            library_prefix = os.environ.get('LIBRARY_PREFIX', library_prefix)

        return library_prefix

#------------------------------------------------------------------------------
# system detection

def is_32bit_environment():
    return not is_64bit_environment()

def is_64bit_environment():
    return sys.maxsize.bit_length() == 63

#------------------------------------------------------------------------------
# CI detection

def is_continuous_integration():
    return 'CI' in os.environ

def is_on_travis():
    return 'TRAVIS' in os.environ

def is_on_appveyor():
    return 'APPVEYOR' in os.environ

