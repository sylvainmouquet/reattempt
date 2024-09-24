from typing import AsyncGenerator

import pytest
from reattempt import reattempt


class RetryException(Exception): ...


@reattempt(max_retries=5, min_time=0.1, max_time=0.2)
async def async_gen_function() -> AsyncGenerator:
    async_gen_function.counter += 1  # type: ignore

    raise RetryException("Error")
    yield 1  # mandator, the function must return a AsyncGenerator


@pytest.mark.asyncio
async def test_retry_async_gen(mocker):
    #mocker.patch("loguru.logger.exception", lambda *args, **kwargs: None)

    async_gen_function.counter = 0  # type: ignore

    with pytest.raises(RetryException) as exc_info:
        async for _conn in async_gen_function():
            break  # Break immediately, as we expect an exception to be raised

    assert str(exc_info.value) == "Error", str(exc_info.value)
    assert async_gen_function.counter == 5  # type: ignore


@pytest.mark.asyncio
async def test_retry_sync(mocker):
    #mocker.patch("loguru.logger.exception", lambda *args, **kwargs: None)

    @reattempt(max_retries=5, min_time=0.1, max_time=0.2)
    def sync_function():
        sync_function.counter += 1  # type: ignore
        raise Exception("failure")

    sync_function.counter = 0  # type: ignore

    try:
        sync_function()
        pytest.fail("Must not come here")
    except Exception:
        print("Success")
    assert sync_function.counter == 5  # type: ignore


@pytest.mark.asyncio
async def test_retry_async(mocker):
    #mocker.patch("loguru.logger.exception", lambda *args, **kwargs: None)

    @reattempt(max_retries=5, min_time=0.1, max_time=0.2)
    async def async_function():
        async_function.counter += 1  # type: ignore
        raise Exception("failure")

    async_function.counter = 0  # type: ignore

    try:
        await async_function()
        pytest.fail("Must not come here")
    except Exception:
        print("Success")
    assert async_function.counter == 5  # type: ignore
