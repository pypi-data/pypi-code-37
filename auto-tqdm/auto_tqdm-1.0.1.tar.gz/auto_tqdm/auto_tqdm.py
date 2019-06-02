from tqdm import tqdm_notebook, tqdm as tqdm_cli
from environments_utils import is_notebook
from typing import Dict, Generator
import humanize

___bars = []


def tqdm(iterable=None, verbose: bool = True, **kwargs: Dict)->Generator:
    """Return adaptative tqdm given the identified environment.
        iterable, object to iterate over.
        verbose:bool, whetever to show the bar or not.
        kwargs:Dict, parameters to pass to the tqdm object.
    """
    if not verbose and iterable is not None:
        return (i for i in iterable)

    global ___bars
    bar = (tqdm_notebook if is_notebook() else tqdm_cli)(iterable, **kwargs)
    ___bars.append(bar)
    return bar


def remaining_time(human: bool = True)->int:
    global ___bars
    total = 1
    completed = 0
    for b in reversed(___bars):
        if b.n >= b.total:
            ___bars.remove(b)
        completed += total*b.n
        total *= b.total
    if not ___bars:
        return None
    avg = ___bars[-1].avg_time
    if avg is None:
        return None
    delta = int(avg*(total-completed))
    return humanize.naturaldelta(delta) if human else delta
