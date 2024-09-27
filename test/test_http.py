from reattempt import reattempt
from test.conftest import MAX_ATTEMPTS, MIN_TIME, MAX_TIME
import pytest
import aiohttp


@reattempt(max_retries=MAX_ATTEMPTS, min_time=MIN_TIME, max_time=MAX_TIME)
async def async_aiohttp_call(status: int):
    async_aiohttp_call.counter += 1  # type: ignore

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://httpbin.org/status/{status}", ssl=False
        ) as response:
            response.raise_for_status()
            return "OK"


@pytest.mark.asyncio
async def test_retry_http_200(disable_logging_exception):
    async_aiohttp_call.counter = 0  # type: ignore

    await async_aiohttp_call(200)
    assert async_aiohttp_call.counter == 1  # type: ignore


@pytest.mark.asyncio
async def test_retry_http_500(disable_logging_exception):
    async_aiohttp_call.counter = 0  # type: ignore

    try:
        await async_aiohttp_call(500)
        pytest.fail("Must not come here")
    except Exception:
        print("Success")
    assert async_aiohttp_call.counter == MAX_ATTEMPTS  # type: ignore
