
# Redirect path
import os

cdir = os.path.dirname(__file__)
pdir = os.path.join(cdir, "../../sconsx")
pdir = os.path.abspath(pdir)

__path__ = [pdir] + __path__[:]

from openalea.sconsx.__init__ import *
