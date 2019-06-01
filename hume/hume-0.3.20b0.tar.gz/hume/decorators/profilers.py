import inspect
import os
import sys
import time
import timeit
from functools import wraps
from contextlib import redirect_stdout
import io
from sty import RgbFg, Sgr, bg, ef, fg, rs


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def explicit():
    """
    Decorator that provides the wrapped function with an attribute 'actual_kwargs'
    containing just those keyword arguments actually passed in to the function.
    """

    def decorator(function):
        defaults = inspect.getcallargs(function)

        def inner(*args, **kwargs):
            inner.defaults = defaults
            if len(args) > 1:
                raise TypeError(
                    "All arguemnts except the first must be keyword arguments (e.g. show_result=True)"
                )
            inner.explicit_args = args
            inner.explicit_kwargs = kwargs
            return function(*args, **kwargs)

        return inner

    return decorator


CONFIG = {}


@explicit()
def profile(
    nums: int = 1,
    *,
    show_args: bool = False,
    show_kwargs: bool = False,
    show_result: bool = False,
    mute_console: bool = False,
):
    """
    A decorator to profile the (average) execution time of functions.
    
    Arguments:
        nums {int} -- the number of times to run the simulation (default: 1)
    Keyword Arguments:
        show_args {bool} -- show the args passed to the function (default: False)
        show_kwargs {bool} -- show the kwargs passed to the function (default: False)
        show_result {bool} -- show the return value of the decorated function (default: False)
        mute_console {bool} -- supress print statements from the decorated function (default: False)
    
    Returns:
        the return value of func(*args, **kwargs) when func() is wrapped 
    """
    # there must be a better way
    try:
        nums = profile.explicit_args[0]
    except IndexError:
        nums = CONFIG.get("nums", profile.defaults.get("nums"))

    item_names = [x for x in profile.defaults.keys() if x != "nums"]
    items = [show_args, show_kwargs, show_result, mute_console]

    for index, (item_name, item_value) in enumerate(zip(item_names, items)):
        items[index] = profile.explicit_kwargs.get(
            item_name, CONFIG.get(item_name, profile.defaults.get(item_name))
        )

    show_args, show_kwargs, show_result, mute_console = items

    def middle(func):
        is_evaluating = False
        # start evaluating recursion after funciton definition
        _, lines = inspect.getsource(func).split(f"{func.__name__}", 1)
        # take the docs out in case they include the function name
        lines = lines.replace(str(func.__doc__), "")

        pre_message = (
            f"\n{fg.green}{ef.b}profiling {func.__name__} {fg.rs}{rs.all}"
        )  # pylint: disable=all

        if func.__name__ in lines:
            pre_message += (
                f"{fg.li_yellow}{ef.b}(recursive function detected) {fg.rs}{rs.all}"
            )

        pre_message += "\n------------------------------------------------"

        print(pre_message, end="")

        def wrapper(*args, **kwargs):
            nonlocal is_evaluating
            f = io.StringIO()
            stdout = ""

            if is_evaluating:
                return func(*args, **kwargs)
            else:

                def timing_func():
                    with HiddenPrints():
                        func(*args, **kwargs)

                is_evaluating = True
                timings = timeit.repeat(stmt=timing_func, repeat=nums, number=1)

                av = sum(timings) / float(len(timings))

                timing_str = f"→ name: {func.__name__}"
                if show_args:
                    timing_str += f"\n→ args: {args}"
                if show_kwargs:
                    timing_str += f"\n→ kwargs: {kwargs}"

                timing_str += (
                    f"\n→ simulations: {nums}\n→ average execution time: {av} seconds"
                )

                with redirect_stdout(f):
                    result = func(*args, **kwargs)
                    stdout += f.getvalue()

                if show_result is True:
                    timing_str += f"\n→ return is: {result}"
                if not mute_console:
                    if stdout.strip():
                        timing_str += f"\n→ console output is: \n{stdout}"
                print("")
                print(timing_str)
                is_evaluating = False
                return result

        return wrapper

    return middle
