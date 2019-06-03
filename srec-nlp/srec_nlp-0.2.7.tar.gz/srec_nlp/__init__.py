__version__ = "0.2.6"
from .srec_nlp import ParallelDots, TextProcessing, Aylien

try:
    from .srec_nlp import FastText
except:
    pass
