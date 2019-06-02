import functools
import itertools
from io import IOBase
from pathlib import Path
from typing import List, Dict, Callable, Union
import copy
import attr
import joblib


@attr.s(frozen=True)
class Score:
    positive: float = attr.ib(factory=float)
    negative: float = attr.ib(factory=float)
    classification: str = ""

    def __attrs_post_init__(self):
        classes = ("positive", "negative")
        filt = [getattr(self, c) for c in classes]
        mx = max(filt)
        object.__setattr__(
            self,
            "classification",
            next(itertools.compress(classes, map(mx.__eq__, filt))),
        )

    @classmethod
    def fromsingle(cls, value):
        """
        :param value: single value score
        :return:
        """
        negative = 1 - value
        positive = value

        return Score(positive=positive, negative=negative)

    @classmethod
    def fromtriplet(cls, positive, neutral, negative):
        """
        :param positive:  Confidence
        :param neutral: Confidence
        :param negative: Confidence
        :return: Score
        """
        positive += neutral / 2
        negative += neutral / 2
        return Score(positive=positive, negative=negative)


@attr.s(frozen=True)
class Query:
    content: str = attr.ib(factory=str)
    score: Score = attr.ib(default=Score())


def _ensure_utf(
    func: Callable[[str], Query]
) -> Callable[[Union[IOBase, str, Path, bytes]], Query]:
    """

    :param func: Query function to wrap
    :return: Returns a wrapper for the provided function.
    """

    @functools.singledispatch
    def _text_is_utf(text: str):
        return text.replace("\n", "")

    @_text_is_utf.register(bytes)
    def _(text: bytes):
        return text.decode("utf-8").replace("\n", "")

    @_text_is_utf.register(Path)
    def _(path: Path):
        text = path.read_text("utf-8").replace("\n", "")
        return text

    @_text_is_utf.register(IOBase)
    def _(fp: IOBase):
        text = "".join(map(str, fp.readlines())).replace("\n", "")
        return text

    @functools.wraps(func)
    def wrapper(self, text):
        text = _text_is_utf(text).replace("\n", "")
        return func(self, text)

    return wrapper


def _parallel(func):
    def listd(self, query):
        query = [(copy.deepcopy(self), q) for q in query]
        return joblib.Parallel()(joblib.delayed(func)(self.copy(), q) for s, q in query)

    @functools.wraps(func)
    def internal(self, query):
        if isinstance(query, list):
            return listd(self, query)
        return func(self, query)

    return internal
