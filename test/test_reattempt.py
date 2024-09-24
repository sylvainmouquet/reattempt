from typing import AsyncGenerator

import pytest

from src.reattempt import reattempt
from test.conftest import MAX_ATTEMPTS, MIN_TIME, MAX_TIME, RetryException


@reattempt(max_retries=MAX_ATTEMPTS, min_time=MIN_TIME, max_time=MAX_TIME)
def sync_function():
    sync_function.counter += 1  # type: ignore
    raise Exception("failure")


@reattempt(max_retries=MAX_ATTEMPTS, min_time=MIN_TIME, max_time=MAX_TIME)
async def async_function():
    async_function.counter += 1  # type: ignore
    raise Exception("failure")


@reattempt(max_retries=MAX_ATTEMPTS, min_time=MIN_TIME, max_time=MAX_TIME)
async def async_gen_function() -> AsyncGenerator:
    async_gen_function.counter += 1  # type: ignore

    raise RetryException("Error")
    yield 1  # mandator, the function must return a AsyncGenerator


@pytest.mark.asyncio
async def test_retry_async_gen(disable_logging_exception):
    async_gen_function.counter = 0  # type: ignore

    with pytest.raises(RetryException) as exc_info:
        async for _conn in async_gen_function():
            break  # Break immediately, as we expect an exception to be raised

    assert str(exc_info.value) == "Error", str(exc_info.value)
    assert async_gen_function.counter == MAX_ATTEMPTS  # type: ignore


@pytest.mark.asyncio
async def test_retry_sync(disable_logging_exception):
    sync_function.counter = 0  # type: ignore

    try:
        sync_function()
        pytest.fail("Must not come here")
    except Exception:
        print("Success")
    assert sync_function.counter == MAX_ATTEMPTS  # type: ignore


@pytest.mark.asyncio
async def test_retry_async(disable_logging_exception):
    async_function.counter = 0  # type: ignore

    try:
        await async_function()
        pytest.fail("Must not come here")
    except Exception:
        print("Success")
    assert async_function.counter == MAX_ATTEMPTS  # type: ignore
