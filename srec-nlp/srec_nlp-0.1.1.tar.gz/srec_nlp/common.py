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
    neutral: float = attr.ib(factory=float)
    negative: float = attr.ib(factory=float)
    classification: str = ''

    def __attrs_post_init__(self):
        classes = ("positive", "neutral", "negative")
        filt = [getattr(self, c) for c in classes]
        mx = max(filt)
        object.__setattr__(self, 'classification', next(itertools.compress(classes, map(mx.__eq__, filt))))


@attr.s(frozen=True)
class Query:
    content: str = attr.ib(factory=str)
    score: Score = attr.ib(default=Score())


def valuetoscore(value: float, negative: float = 0.0, neutral: float = 0.5, positive: float = 1.0):
    """
    :param value: single value'd score
    :param negative: value around which negatives exist
    :param neutral: value around which neutrals exist
    :param positive: value around which positives exist
    :return:
    """

    @functools.lru_cache(32)
    def make_gaussian(b) -> Callable[[float], Callable[[float], float]]:
        """
        Stage constructor for gaussian
        :param b: The center of the gaussian
        :return: A callable that takes the std dev and returns a gaussian function.
        """
        return lambda c: lambda x: 2.72 ** ((-(x - b) ** 2) / (2 * c ** 2 + 1e-4))

    def minmax(v: List[float]) -> (float, float):
        return min(v), max(v)

    @functools.lru_cache(32)
    def from_single_internal(negative_base: float, neutral_base: float, positive_bays: float) -> Dict[str, float]:
        def calc_error(c):
            neg = make_gaussian(negative_base)(c)
            neut = make_gaussian(neutral_base)(c)
            pos = make_gaussian(positive_bays)(c)

            def sum_of_gaussians(x):
                return pos(x) + neg(x) + neut(x)

            mi, ma = minmax((negative_base, positive_bays, neutral_base))
            v = np.array(list(map(sum_of_gaussians, np.arange(mi, ma, 1e-4))))
            return mean_squared_error(np.ones_like(v), v)

        optim = minimize_scalar(calc_error, bounds=(1e-6, 1)).x
        return {
            "positive": make_gaussian(positive_bays)(optim)(value),
            "neutral": make_gaussian(neutral_base)(optim)(value),
            "negative": make_gaussian(negative_base)(optim)(value),
        }

    scoring = from_single_internal(negative, neutral, positive)
    return Score(**scoring)


def _ensure_utf(func: Callable[[str], Query]) -> Callable[[Union[IOBase, str, Path, bytes]], Query]:
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
        text = bytes("".join(map(str, fp.readlines()))).decode("utf-8")
        return text

    @functools.wraps(func)
    def wrapper(self, text):
        text = _text_is_utf(text)
        return func(self, text)

    return wrapper
