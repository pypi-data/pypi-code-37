"""Query evaluation unit tests."""

from datalog.core import (Constant, Dataset, LVar, Rule, evaluate, read,
                          simple_eval)


def test_id_query():
  """Querying for a constant in the dataset."""

  ab = (Constant("a"), Constant("b"),)
  assert not simple_eval(Dataset([], []), ("a", "b",))
  assert simple_eval(Dataset([ab], []), ("a", "b",)) == \
      [(("a", "b"), {},)]


def test_lvar_query():
  """Querying for a binding in the dataset."""

  d = read("""a(b). a(c).""")

  assert simple_eval(d, ("a", "X")) == \
      [(("a", "b"), {"X": "b"}),
       (("a", "c"), {"X": "c"})]


def test_lvar_unification():
  """Querying for MATCHING bindings in the dataset."""

  d = read("""edge(b, c). edge(c, c).""")

  assert simple_eval(d, ("edge", "X", "X",)) == \
      [(("edge", "c", "c"), {"X": "c"})]


def test_rule_join():
  """Test a basic join query - the parent -> grandparent relation."""

  child = Constant("child")
  gc = Constant("grandchild")

  d = read("""
child(a, b).
child(b, c).
child(b, d).
child(b, e).

grandchild(A, B) :-
  child(A, C),
  child(C, B).
""")

  assert simple_eval(d, ("grandchild", "a", "X",)) == \
      [(("grandchild", "a", "c"), {"X": "c"}),
       (("grandchild", "a", "d"), {"X": "d"}),
       (("grandchild", "a", "e"), {"X": "e"})]


def test_antijoin():
  """Test a query containing an antijoin."""

  d = read("""
a(foo, bar).
b(foo, bar).
a(baz, qux).
% matching b(baz, qux). is our antijoin test

no-b(X, Y) :-
  a(X, Y),
  ~b(X, Z).
""")

  assert simple_eval(d, ("no-b", "X", "Y")) == \
      [(("no-b", "baz", "qux"),
        {"X": "baz",
         "Y": "qux"})]


def test_nested_antijoin():
  """Test a query which negates a subquery which uses an antijoin.

  Shouldn't exercise anything more than `test_antjoin` does, but it's an interesting case since you
  actually can't capture the same semantics using a single query. Antijoins can't propagate positive
  information (create lvar bindings) so I'm not sure you can express this another way without a
  different evaluation strategy.

  """

  d = read("""
a(foo, bar).
b(foo, bar).
a(baz, qux).
b(baz, quack).

b-not-quack(X, Y) :-
  b(X, Y),
  ~=(Y, quack).

a-no-nonquack(X, Y) :-
  a(X, Y),
  ~b-not-quack(X, Y).
""")

  assert simple_eval(d, ("a-no-nonquack", "X", "Y")) == \
      [(("a-no-nonquack", "baz", "qux"),
        {"X": "baz",
          "Y": "qux"})]


def test_alternate_rule():
  """Testing that both recursion and alternation work."""

  d = read("""
edge(a, b).
edge(b, c).
edge(c, d).
edge(d, e).
edge(e, f).

path(A, B) :-
  edge(A, B).

path(A, B) :-
  edge(A, C),
  path(C, B).
""")

  # Should be able to recurse to this one.
  assert simple_eval(d, ("path", "a", "f")) == \
      [(("path", "a", "f"), {})]
