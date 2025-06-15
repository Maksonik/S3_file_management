import functools
import inspect
import json
import time
from collections import OrderedDict
from collections.abc import Callable
from typing import Any, ParamSpecArgs, ParamSpecKwargs


def hash_args_kwargs(*args: ParamSpecArgs, **kwargs: ParamSpecKwargs) -> int:
    try:
        combined = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
        return hash(combined)
    except TypeError:
        return hash(functools._make_key(args, kwargs, True))  # noqa: FBT003, SLF001


def async_cache(ttl: int = None, max_size: int = 20) -> Callable:
    """
    Decorator for caching result from async functions with optional TTL (seconds)
    """

    def decorator(func: Callable) -> Callable:
        cache = OrderedDict()

        @functools.wraps(func)
        async def wrapper(*args: ParamSpecArgs, **kwargs: ParamSpecKwargs) -> Any:  # noqa: ANN401
            is_method = (
                len(args) > 0
                and hasattr(args[0], func.__name__)
                and inspect.ismethod(getattr(args[0], func.__name__, None))
            )

            fix_args = (f"{args[0].__class__.__module__}, {func.__name__}", *args[1:]) if is_method else args

            key = hash_args_kwargs(fix_args, **kwargs)
            now = time.monotonic()
            if key in cache and (not ttl or now - cache[key]["time"] < ttl):
                return cache[key]["result"]
            result = await func(*args, **kwargs)
            cache[key] = {"time": now, "result": result}
            if len(cache) > max_size:
                cache.popitem(last=False)
            return result

        return wrapper

    return decorator
