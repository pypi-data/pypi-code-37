__license__ = "ISC"
__author__ = "David Kalliecharan"
__author_email__ = "david@david.science"

try:
    from .xps import *

except ImportError as err:
    print(err)
	
