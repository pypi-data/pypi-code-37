"""Query evaluation unit tests."""

from pprint import pprint

from datalog.core import Dataset, Constant, LVar, Rule, evaluate, read


def test_id_query():
  """Querying for a constant in the dataset."""

  c = (Constant("a"), Constant("b"),)
  assert not list(evaluate(Dataset([], []), c))
  assert list(evaluate(Dataset([c], []), c)) == [(c, {},)]


def test_lvar_query():
  """Querying for a binding in the dataset."""

  d = read("""a(b). a(c).""")

  x = LVar("X")
  assert list(evaluate(d, (Constant("a"), x,))) == \
    [((Constant("a"), Constant("b")), {x: Constant("b")}),
     ((Constant("a"), Constant("c")), {x: Constant("c")})]


def test_lvar_unification():
  """Querying for MATCHING bindings in the dataset."""

  d = read("""edge(b, c). edge(c, c).""")

  x = LVar("X")
  assert list(evaluate(d, (Constant("edge"), x, x,))) == \
    [((Constant("edge"), Constant("c"), Constant("c")), {x: Constant("c")})]


def test_rule_join():
  """Test a basic join query - the parent -> grandparent relation."""

  child = Constant("child")
  gc = Constant("grandchild")
  grandchild = Rule((gc, LVar("A"), LVar("B")),
                    [(child, LVar("A"), LVar("C")),
                     (child, LVar("C"), LVar("B"))])

  d = read("""
child(a, b).
child(b, c).
child(b, d).
child(b, e).

grandchild(A, B) :-
  child(A, C),
  child(C, B).
""")

  print(d)

  assert list(evaluate(d, (gc, Constant("a"), LVar("X")))) == \
    [((gc, Constant("a"), Constant("c")), {LVar("X"): Constant("c")}),
     ((gc, Constant("a"), Constant("d")), {LVar("X"): Constant("d")}),
     ((gc, Constant("a"), Constant("e")), {LVar("X"): Constant("e")})]


def test_antijoin():
  """Test a query containing an antijoin."""

  a = lambda x, y: (Constant("a"), Constant(x), Constant(y))
  b = lambda x, y: (Constant("b"), Constant(x), Constant(y))

  d = read("""
a(foo, bar).
b(foo, bar).
a(baz, qux).
% matching b(baz, qux). is our antijoin test

no-b(X, Y) :-
  a(X, Y),
  ~b(X, Z).
""")

  assert list(evaluate(d, (Constant("no-b"), LVar("X"), LVar("Y")))) == \
    [((Constant("no-b"), Constant("baz"), Constant("qux")),
      {LVar("X"): Constant("baz"),
       LVar("Y"): Constant("qux")})]


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
  assert list(evaluate(d, (Constant("path"), Constant("a"), Constant("f")))) == \
    [((Constant("path"), Constant("a"), Constant("f")), {})]
