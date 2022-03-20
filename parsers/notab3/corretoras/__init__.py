from .Mirae2013 import mirae_2013
from .Mirae2014 import mirae_2014
from .Socopa2013 import socopa_2013

readers = {}

readers.update(mirae_2013)
readers.update(mirae_2014)
readers.update(socopa_2013)
