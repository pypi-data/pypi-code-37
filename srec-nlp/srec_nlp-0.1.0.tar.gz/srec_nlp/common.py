import dataclasses
from typing import Union, List
from pathlib import Path


import six


def _make_input_utf(func):
    def internal(self, text: Union[str, bytes, Path], *vargs, **kwargs):

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        elif isinstance(text, Path):
            with text.open("r", encoding="utf-8") as fp:
                text = "".join(fp.readlines())

        return func(self, text, *vargs, **kwargs)

    return internal


@dataclasses.dataclass
class Query:
    content: Union[str, List["Query"]]
    score: int


def NLP(clazz):
    def notimp(func_name):
        def notimp_internal(*vargs, **kwargs):
            raise NotImplementedError(
                f"Function {func_name} is not implemented for class {clazz}."
            )
        return notimp_internal

    clazz.analyze = _make_input_utf(getattr(clazz, "analyze", notimp("analyze")))

    return clazz

