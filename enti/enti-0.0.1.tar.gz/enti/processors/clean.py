import re
from enti.api.processor import *
from enti.steps import *

__all__ = [
    "sentence_boundary_fix",
    "suppress_read_less",
    "suppress_paren",
    "suppress_bracket",
    "suppress_all",
    "clean_all"
]
sentence_boundary_fix = RegexSubstitution(
    "sentence-boundary-fix",
    re.compile(r"([^A-Z])[.]([A-Z])"),
    r"\1. \2"
)
suppress_read_less = RegexSubstitution(
    "suppress-read-less",
    re.compile(r"Read less\.+"),
    ""
)
suppress_paren = RegexSubstitution(
    "suppress-paren",
    re.compile(r"[(][^()]+[)]"),
    ""
)
suppress_bracket = RegexSubstitution(
    "suppress-bracket",
    re.compile(r"[[][^[\]]+[\]]"),
    ""
)


def _builder(pipeline_id, steps, prefix=None):
    processors = []
    idx = 0
    for s in steps:
        if len(s) == 2:
            if prefix:
                id = f"{prefix}-{idx:02d}"
            else:
                id = f"{pipeline_id}-{idx:02d}"
            pattern = s[0]
            repl = s[1]
        elif len(s) == 3:
            id, pattern, repl = s
        else:
            raise Exception()
        processors.append(
            (id, pattern, repl)
        )
        idx+=1
    processors = [RegexSubstitution(a, b, c)
                  for a, b, c in processors]
    return Pipeline(pipeline_id, processors)



fix_quotes = _builder(
    pipeline_id="char-repl",
    steps=[
        (re.compile("[‘’]"),"'"),
        (re.compile("[“”]"),"\""),
        (re.compile("[–]"),"-"),
        (re.compile("\t|\n")," "),
        (re.compile(" {2,}")," "),
        (re.compile("'([A-Za-z ])'"),r"\1"),
    ]
)

suppress_all = Pipeline(
    id="suppress-all",
    steps=[
        suppress_read_less,
        suppress_paren,
        suppress_bracket,

    ]
)

clean_all = Pipeline(
    id="regex-clean",
    steps=[
        sentence_boundary_fix,
        words_to_numeric,
        suppress_all,
        fix_quotes
    ]
)