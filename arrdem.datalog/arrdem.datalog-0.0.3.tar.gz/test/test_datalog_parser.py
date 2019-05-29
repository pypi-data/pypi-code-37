from pprint import pprint

from datalog.parser import parse
from datalog.core import Actions

import pytest

EXS = [
    "%foo\n",
    """a(b).""",
    """edge(a).""",
    """a(b, c).""",
    """edge(smfc-ait, smfc).""",
    """edge("smfc-ait", smfc).""",
    """path(A, B) :- edge(A, C), path(C, B).""",
    """path(A, B) :-
  edge(A, C),
  path(C, B).""",
    """path(A, B) :- % one comment
  edge(A, C), % the next
  path(C, B).""",
  """foo(A, B) :-
  ~bar(A, B),
  qux(A, B)."""
]

@pytest.mark.parametrize('ex,', EXS)
def test_parser(ex):
  assert parse(ex, actions=Actions())
