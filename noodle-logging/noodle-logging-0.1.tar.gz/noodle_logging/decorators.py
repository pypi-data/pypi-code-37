import time
import json
from functools import wraps


from .logger import log
from .utils import generate_unique_id


def profile(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        _id = generate_unique_id()
        args_str = ','.join([str(e) for e in args])
        kwargs_str = json.dumps(kwargs)
        timestamp_start = time.time()
        log.info(
            "Function Profiler",
            fn_name=func.__name__,
            fn_id=_id,
            timestamp_start=timestamp_start,
            fn_args=args_str,
            fn_kwargs=kwargs_str
        )
        result = func(*args, **kwargs)
        timestamp_end = time.time()
        log.info(
            "Function Profiler",
            fn_name=func.__name__,
            fn_id=_id,
            timestamp_start=timestamp_start,
            fn_args=args_str,
            fn_kwargs=json.dumps(kwargs),
            timestamp_end=timestamp_end,
            exec_time=timestamp_end - timestamp_start
        )
        return result

    return wrapper


def log_exceptions(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:

            args_str = ','.join([str(e) for e in args])
            kwargs_str = json.dumps(kwargs)
            err = "There was an exception in  ", func.__name__
            log.exception(
                "Exception Found.",
                exception=err,
                fn_args=args_str,
                fn_kwargs=kwargs_str
            )
            raise

    return wrapper
