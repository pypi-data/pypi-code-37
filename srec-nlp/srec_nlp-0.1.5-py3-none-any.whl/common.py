import functools
import itertools
from io import IOBase
from pathlib import Path
from typing import List, Dict, Callable, Union

import attr
import numpy as np
from scipy.optimize import minimize_scalar
from sklearn.metrics import mean_squared_error


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
        return text

    @_text_is_utf.register
    def _(text: bytes):
        return text.decode("utf-8")

    @_text_is_utf.register
    def _(path: Path):
        text = "".join(path.open("r", encoding="utf-8").readlines())
        return text

    @_text_is_utf.register
    def _(fp: IOBase):
        text = "".join(map(str, fp.readlines()))
        return text

    @functools.wraps(func)
    def wrapper(self, text):
        text = _text_is_utf(text)
        return func(self, text)

    return wrapper
