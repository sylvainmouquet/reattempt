__version__ = "1.1.2"
__all__ = ("__version__", "reattempt")

import asyncio
import contextlib
import functools
import inspect
import logging
import random
import time
from typing import Callable, TypeVar, Optional, Any, Union, cast

# Type variables for better type hinting
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

# Constants
CONST_DEFAULT_MAX_RETRIES: int = 5
CONST_DEFAULT_MIN_TIME: float = 0.1
CONST_DEFAULT_MAX_TIME: float = 0.2

# Setup logging
logger = logging.getLogger("reattempt")
logger.addHandler(logging.NullHandler())


def reattempt(
    func: Optional[Callable[..., Any]] = None,
    max_retries: int = CONST_DEFAULT_MAX_RETRIES,
    min_time: float = CONST_DEFAULT_MIN_TIME,
    max_time: float = CONST_DEFAULT_MAX_TIME,
):
    """
    Decorator to retry a function upon failure with exponential backoff.

    This decorator can be used to wrap any function that may fail intermittently. It will retry the function
    a specified number of times, with an exponentially increasing delay between retries.

    Parameters:
    -----------
    func : callable, optional
        The function to be decorated.

    max_retries : int, optional
        The maximum number of times to retry the function upon failure. Default is CONST_DEFAULT_MAX_RETRIES.

    min_time : float, optional
        The minimum time (in seconds) to wait before the first retry. Default is CONST_DEFAULT_MIN_TIME.

    max_time : float, optional
        The maximum time (in seconds) to wait between retries. Default is CONST_DEFAULT_MAX_TIME.

    Returns:
    --------
    callable
        A decorated function that includes retry logic with exponential backoff.

    Example:
    --------
    @reattempt(max_retries=5, min_time=1, max_time=10)
    def my_function():
        # Function logic that may fail intermittently
        pass

    Notes:
    ------
    - The delay between retries is calculated using an exponential backoff strategy.
    - If the function succeeds on any attempt, it will return the result immediately.
    - If the function fails after the maximum number of retries, the last exception will be raised.
    """

    # Helper functions for retry logic
    def _get_wait_time(current_wait: float) -> float:
        return random.uniform(current_wait, max_time)

    def _log_attempt_failure(attempt: int, wait_time: float) -> None:
        if attempt + 1 == max_retries:
            logger.warning(f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, stopping")
        else:
            logger.warning(
                f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, "
                f"retrying in {format(wait_time, '.2f')} seconds..."
            )

    def _log_max_retries_reached() -> None:
        logger.error("[RETRY] Max retries reached")

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            wait_time: float = min_time
            attempt: int = 0  # attempt: tentative
            # Capture the latest exception to raise it at the end
            capture_exception: Exception | None = None

            while attempt < max_retries:
                wait_time = _get_wait_time(wait_time)

                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.exception(e)
                    capture_exception = e
                    _log_attempt_failure(attempt, wait_time)
                    attempt += 1
                    await asyncio.sleep(wait_time)

            if attempt == max_retries:
                _log_max_retries_reached()
                if capture_exception:
                    raise capture_exception

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            wait_time: float = min_time
            attempt: int = 0  # attempt: tentative
            # Capture the latest exception to raise it at the end
            capture_exception: Exception | None = None

            while attempt < max_retries:
                wait_time = _get_wait_time(wait_time)

                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.exception(e)
                    capture_exception = e
                    _log_attempt_failure(attempt, wait_time)
                    attempt += 1
                    time.sleep(wait_time)

            if attempt == max_retries:
                _log_max_retries_reached()
                if capture_exception:
                    raise capture_exception

        @functools.wraps(func)
        async def async_gen_wrapper(*args, **kwargs):
            wait_time: float = min_time

            # Capture the latest exception to raise it at the end
            capture_exception: Exception | None = None

            attempt: int = 0
            should_retry: bool = True
            item = None

            while should_retry and attempt < max_retries:
                wait_time = _get_wait_time(wait_time)

                try:
                    item = None
                    async with contextlib.aclosing(func(*args, **kwargs)) as agen:
                        # https://docs.python.org/3/library/contextlib.html#contextlib.aclosing
                        # https://docs.python.org/3/reference/expressions.html#asynchronous-generator-functions
                        async for item in agen:
                            yield item
                    break
                except Exception as e:
                    # exception captured are not specific to this code, we capture all exceptions of the program
                    # logging.exception(e)

                    capture_exception = e

                    if not item:  # the instanciation has failed
                        logging.exception(e)
                        _log_attempt_failure(attempt, wait_time)
                        attempt = attempt + 1
                        await asyncio.sleep(wait_time)
                    else:
                        should_retry = False

            if attempt == max_retries:
                _log_max_retries_reached()

                if capture_exception:
                    raise capture_exception

            # for exceptions out of the scope of the gen
            if capture_exception and not should_retry:
                raise capture_exception

        @functools.wraps(func)
        def sync_gen_wrapper(*args, **kwargs):
            wait_time: float = min_time
            attempt: int = 0
            should_retry: bool = True
            capture_exception: Exception | None = None

            while should_retry and attempt < max_retries:
                wait_time = random.uniform(wait_time, max_time)

                item = None
                try:
                    with contextlib.closing(func(*args, **kwargs)) as agen:
                        for item in agen:
                            yield item
                    break
                except Exception as e:
                    capture_exception = e

                    if not item:  # the instantiation has failed
                        logging.exception(e)
                        _log_attempt_failure(attempt, wait_time)
                        attempt = attempt + 1
                        time.sleep(wait_time)
                    else:
                        should_retry = False

            if attempt == max_retries:
                _log_max_retries_reached()

                if capture_exception:
                    raise capture_exception

            # for exceptions out of the scope of the gen
            if capture_exception and not should_retry:
                raise capture_exception

        # Determine the type of function and return the appropriate wrapper
        if inspect.iscoroutinefunction(func):
            return cast(F, async_wrapper)
        elif inspect.isasyncgenfunction(func):
            return cast(F, async_gen_wrapper)
        elif inspect.isgeneratorfunction(func):
            return cast(F, sync_gen_wrapper)
        return cast(F, sync_wrapper)

    if func is None:
        return decorator
    return decorator(func)
