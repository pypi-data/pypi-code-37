__version__ = "0.1.3"
from .srec_nlp import ParallelDots, TextProcessing, Aylien

try:
    from .srec_nlp import FastText
except:
    pass
