"""
A datalog engine.
"""

import logging as log
import sys
from collections import namedtuple
from functools import reduce
from itertools import chain
# class MockLog(object):
#   def debug(self, msg):
#     print(msg)
# log = MockLog()
from random import shuffle

from .parser import parse

##################################################
# Types


class Dataset(namedtuple("Dataset", ["tuples", "rules"])):
  """A set of tuples and rules which can be queried."""

  def merge(self, other):
    """Merge two datasets together, returning a new one."""

    return Dataset(list({*self.tuples, *other.tuples}),
                   (self.rules or []) + (other.rules or []))


class Constant(namedtuple("Constant", ["value"])):
  def pr_str(self):
    return self.value


class LVar(namedtuple("LVar", ["name"])):
  def pr_str(self):
    return self.name


class Rule(namedtuple("Rule", ["pattern", "clauses"])):
  def pr_str(self):
    return pr_str(self.pattern) + " :- " + ", ".join(pr_str(c) for c in self.clauses) + "."


def pr_str(v):
  if isinstance(v, (Constant, LVar, Rule,)):
    return v.pr_str()
  elif isinstance(v, tuple):
    return pr_str(v[0]) + "(" + (", ".join(repr(pr_str(e)) for e in v[1:])) + ")"
  else:
    return repr(v)


####################################################################################################
# The reader

##################################################
# The parser's hooks


class Actions(object):
  def make_dataset(self, input, start, end, elements):
    # Group the various terms
    rules = []
    tuples = []
    for e in elements:
      if e:
        if isinstance(e, Rule):
          rules.append(e)
        else:
          tuples.append(e)

    return Dataset(tuples, rules)

  def make_symbol(self, input, start, end, elements):
    return LVar("".join(e.text for e in elements),)

  def make_word(self, input, start, end, elements):
    return Constant("".join(e.text for e in elements),)

  def make_string(self, input, start, end, elements):
    return Constant(elements[1].text,)

  def make_comment(self, input, start, end, elements):
    return None

  def make_ws(self, input, start, end, elements=None):  # watf?
    pass

  def make_rule(self, input, start, end, elements):
    if elements[1].elements:
      return Rule(elements[0], elements[1].elements[3][1])
    else:
      return elements[0]

  def make_clause(self, input, start, end, elements):
    if elements[0].text == "~":
      return ("not", (elements[1], *elements[3][1]))
    else:
      return (elements[1], *elements[3][1])

  def make_terms(self, input, start, end, elements):
    return self._make("terms", elements)

  def make_clauses(self, input, start, end, elements):
    return self._make("clauses", elements)

  def _make(self, tag, elements):
    if len(elements) == 1:
      return (tag, [elements[0]],)
    elif elements[1].elements:
      return (tag, [elements[0]] + elements[1].elements[2][1])
    else:
      return (tag, [elements[0]])


##################################################
# Helpers
def read(text: str):
  """Read a string of text, returning a datalog tree."""

  return parse(text, actions=Actions())

####################################################################################################
# Query evaluation


def shuffled(seq):
  """Because random.shuffle() is in-place >.>"""
  s = seq.copy()
  shuffle(s)
  return s


def constexpr_p(expr):
  """Predicate. True of all terms of the expr are constants."""

  return all(isinstance(e, LVar) for e in expr)


def match(tuple, expr, bindings=None):
  """Attempt to construct lvar bindings from expr such that tuple and expr equate.

  If the match is successful, return the binding map, otherwise return None.
  """

  bindings = bindings.copy() if bindings is not None else {}
  for a, b in zip(expr, tuple):
    # Note the lvar - lvar case is deliberately ignored.
    # This may not work out long term.
    if isinstance(a, LVar) and isinstance(b, LVar):
      continue
    elif isinstance(a, LVar) and not a in bindings and isinstance(b, Constant):
      bindings[a] = b
    elif isinstance(a, LVar) and a in bindings and bindings[a] == b:
      continue
    elif isinstance(a, LVar) and a in bindings and bindings[a] != b:
      return
    elif a != b:
      return

  return bindings


def apply_bindings(expr, bindings, strict=True):
  """Given an expr which may contain lvars, substitute its lvars for constants returning the
  simplified expr.

  """

  if strict:
    return tuple((bindings[e] if isinstance(e, LVar) else e) for e in expr)
  else:
    return tuple((bindings.get(e, e) if isinstance(e, LVar) else e) for e in expr)

# Here we go mutually recursive evaluation....


def evaluate(db: Dataset, expr, bindings=None, cache=None, _recursion_guard=None):
  """Evaluate an expression in a database, lazily producing a sequence of 'matching' tuples.

  The dataset is a set of tuples and rules, and the expression is a single tuple containing lvars
  and constants. Evaluates rules and tuples, returning

  """

  # FIXME (arrdem 2019-05-26):
  #   Obvious optimization - index by "table" so that scans can be reduced

  if cache is None:
    cache = []

  if _recursion_guard is None:
    _recursion_guard = set()

  if bindings is None:
    bindings = {}

  # Binary equality is built-in and somewhat magical.
  if expr[0] == Constant("=") and len(expr) == 3:
    e = apply_bindings(expr, bindings)
    if e[1] == e[2]:
      yield (expr, bindings)

  elif constexpr_p(expr) and expr in db.tuples:
    # The only possible matching tuple is the tuple itself.
    log.debug(f"[constants] {expr} yielded itself")
    yield (expr, bindings or {})

  else:
    # We have a query with lvars
    for t in chain(db.tuples, cache):
      _bindings = match(t, expr, bindings or {})
      if _bindings is not None:
        log.debug(f"[tuples] {expr} yielded {t}")
        yield (t, _bindings)

    # And now for the messy bit, we have to do rule evaluation.
    for r in db.rules:
      # HACK (arrdem 2019-05-27):
      #   To prevent infinite right-recursion, truncate on "table" so we only recur when needed.
      if r.pattern[0] == expr[0] and id(r.pattern) not in _recursion_guard:
        # Establish "base" bindings from expr constants to rule lvars
        base_bindings = match(expr, r.pattern) or {}
        for bindings in join(db, r.pattern, r.clauses, base_bindings,
                             cache=cache, _recursion_guard={id(r.pattern), *_recursion_guard}):
          # And some fancy footwork so we return bindings in terms of THIS expr not the pattern(s)
          t = apply_bindings(r.pattern, bindings)
          p_bindings = match(t, expr)
          # It's possible that we bind a tuple, and then it doesn't match.
          # It's also possible that we re-computed a tuple.
          if p_bindings is not None and t not in cache:
            cache.append(t)
            log.debug(f"[rules] {r.pattern} yielded {t}")
            yield (t, p_bindings,)


def join(db: Dataset, pattern, clauses, bindings, cache=None, _recursion_guard=None):
  """Evaluate clauses over the dataset, joining (or antijoining) with the seed bindings.

  Yields a sequence of bindings for which all joins and antijoins were satisfied.
  """

  if cache is None:
    cache = []

  def __join(g, clause):
    for bindings in g:
      log.debug(f"{pattern} __join {clause} with {bindings}")
      for _, _bindings in evaluate(db, clause, bindings,
                                   cache=cache, _recursion_guard=_recursion_guard):
        log.debug(f"{pattern} __joined {clause} with {_bindings}")
        yield {**bindings, **_bindings}

  def __antijoin(g, clause):
    clause = clause[1]
    for bindings in g:
      log.debug(f"{pattern} __antijoin {clause} {bindings}")
      if not any(evaluate(db, apply_bindings(clause, bindings, strict=False),
                          cache=cache, _recursion_guard=_recursion_guard)):
        log.debug(f"{pattern} __antijoin {clause} with {bindings}")
        yield bindings

  def _join(g, clause):
    if clause[0] == "not":
      return __antijoin(g, clause)
    else:
      return __join(g, clause)

  def _eval(init, bindings):
    for _, bindings in evaluate(db, init,
                                bindings=bindings,
                                cache=cache, _recursion_guard=_recursion_guard):
      yield bindings

  # Get the "first" clause which is a positive join - as these can be selects
  # and pull all antijoins so they can be sorted to the "end" as a proxy for dependency ordering
  init = None
  join_clauses = []
  antijoin_clauses = []
  for c in clauses:
    if c[0] != "not" and not init:
      init = c
    elif c[0] == "not":
      antijoin_clauses.append(c)
    else:
      join_clauses.append(c)

  # The iterator is the chained application of _join over all the clauses, seeded with the init gen.
  for bindings in reduce(_join,
                         join_clauses + antijoin_clauses,
                         _eval(init, bindings)):
    log.debug(f"{pattern} yielded {bindings}")
    yield bindings
