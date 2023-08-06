from functools import wraps
import asyncio


def async_to_sync(fn):
    """
    Returns a synchronous version of an async function, which you can then call without much boilerplate.

    :param fn:
    :return:
    """
    @wraps(fn)
    def __logic(self, *args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(fn(self, *args, **kwargs))
    return __logic
