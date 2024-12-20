__version__ = "1.1.2"
__all__ = ("__version__", "reattempt")

import asyncio
import contextlib
import functools
import inspect
import logging
import random
import time
from collections.abc import Callable, Generator, AsyncGenerator
from typing import Any, TypeVar, Union, Optional

T = TypeVar("T")

CONST_DEFAULT_MAX_RETRIES: int = 5
CONST_DEFAULT_MIN_TIME: float = 0.1
CONST_DEFAULT_MAX_TIME: float = 0.2

logger = logging.getLogger("reattempt")
logger.addHandler(logging.NullHandler())


def reattempt(
    func: Optional[Callable[..., Any]] = None,
    max_retries: int = CONST_DEFAULT_MAX_RETRIES,
    min_time: float = CONST_DEFAULT_MIN_TIME,
    max_time: float = CONST_DEFAULT_MAX_TIME,
) -> Callable[..., Any]:
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

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def retry_async_func(*args: Any, **kwargs: Any) -> Any:
            wait_time: float = min_time
            attempt: int = 0
            capture_exception: Optional[Exception] = None

            while attempt < max_retries:
                wait_time = random.uniform(wait_time, max_time)

                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.exception(e)
                    capture_exception = e

                    if attempt + 1 == max_retries:
                        logging.warning(
                            f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, stopping"
                        )
                    else:
                        logging.warning(
                            f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, retrying in {format(wait_time, '.2f')} seconds..."
                        )

                    attempt += 1
                    await asyncio.sleep(wait_time)

            if attempt == max_retries:
                logging.error("[RETRY] Max retries reached")
                raise capture_exception

        @functools.wraps(func)
        def retry_sync_func(*args: Any, **kwargs: Any) -> Any:
            wait_time: float = min_time
            attempt: int = 0
            capture_exception: Optional[Exception] = None

            while attempt < max_retries:
                wait_time = random.uniform(wait_time, max_time)

                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.exception(e)
                    capture_exception = e

                    if attempt + 1 == max_retries:
                        logging.warning(
                            f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, stopping"
                        )
                    else:
                        logging.warning(
                            f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, retrying in {format(wait_time, '.2f')} seconds..."
                        )

                    attempt += 1
                    time.sleep(wait_time)

            if attempt == max_retries:
                logging.error("[RETRY] Max retries reached")
                raise capture_exception

        @functools.wraps(func)
        async def retry_async_gen_func(*args: Any, **kwargs: Any) -> AsyncGenerator[Any, None]:
            wait_time: float = min_time
            capture_exception: Optional[Exception] = None
            attempt: int = 0
            should_retry: bool = True
            item: Optional[Any] = None

            while should_retry and attempt < max_retries:
                wait_time = random.uniform(wait_time, max_time)

                try:
                    item = None
                    async with contextlib.aclosing(func(*args, **kwargs)) as agen:
                        # https://docs.python.org/3/library/contextlib.html#contextlib.aclosing
                        async for item in agen:
                            yield item
                    break
                except Exception as e:
                    capture_exception = e

                    if not item:
                        logging.exception(e)

                        if attempt + 1 == max_retries:
                            logging.warning(
                                f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, stopping"
                            )
                        else:
                            logging.warning(
                                f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, retrying in {format(wait_time, '.2f')} seconds..."
                            )

                        attempt += 1
                        await asyncio.sleep(wait_time)
                    else:
                        should_retry = False

            if attempt == max_retries:
                logging.error("[RETRY] Max retries reached")
                raise capture_exception

            if capture_exception and not should_retry:
                raise capture_exception

        @functools.wraps(func)
        def retry_sync_gen_func(*args: Any, **kwargs: Any) -> Generator[Any, None, None]:
            wait_time: float = min_time
            attempt: int = 0
            should_retry: bool = True
            capture_exception: Optional[Exception] = None

            while should_retry and attempt < max_retries:
                wait_time = random.uniform(wait_time, max_time)

                try:
                    item = None
                    with contextlib.closing(func(*args, **kwargs)) as agen:
                        for item in agen:
                            yield item
                    break
                except Exception as e:
                    capture_exception = e

                    if not item:
                        logging.exception(e)

                        if attempt + 1 == max_retries:
                            logging.warning(
                                f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, stopping"
                            )
                        else:
                            logging.warning(
                                f"[RETRY] Attempt {attempt + 1}/{max_retries} failed, retrying in {format(wait_time, '.2f')} seconds..."
                            )

                        attempt += 1
                        time.sleep(wait_time)
                    else:
                        should_retry = False

            if attempt == max_retries:
                logging.error("[RETRY] Max retries reached")
                raise capture_exception

            if capture_exception and not should_retry:
                raise capture_exception

        if inspect.iscoroutinefunction(func):
            return retry_async_func
        elif inspect.isasyncgenfunction(func):
            return retry_async_gen_func
        elif inspect.isgeneratorfunction(func):
            return retry_sync_gen_func
        return retry_sync_func

    if func:
        return decorator(func)
    return decorator
