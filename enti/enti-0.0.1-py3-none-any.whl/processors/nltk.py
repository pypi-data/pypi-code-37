

from nltk import sent_tokenize, word_tokenize, ne_chunk, pos_tag, parse_sents
from nltk.treeprettyprinter import TreePrettyPrinter

from enti.api.processor import *


nltk_sent_tokenize = Processor(
    id="nltk-s-tokenizer",
    method=sent_tokenize
)
nltk_sent_chunk = Processor(
    id="nltk-s-chunk",
    method=ne_chunk
)
nltk_word_tokenize = Processor(
    id="nltk-s-tokenize",
    method=word_tokenize
)
nltk_pos_tag = Processor(
    id="nltk-pos-tag",
    method=pos_tag
)


def _pprint_tree(data):
    sentence = data["headline"]
    tree = data["chunks"]
    tpp = TreePrettyPrinter(tree)
    text = tpp.text()
    print(text)
    return text

nltk_display_tree = Processor(
    id="nltk-display-tree",
    method=_pprint_tree
)

