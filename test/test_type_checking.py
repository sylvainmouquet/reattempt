import pytest
from reattempt import reattempt
from test.conftest import RetryException


@reattempt
def retry_function_without_parenthesis():
    retry_function_without_parenthesis.counter += 1  # type: ignore
    if retry_function_without_parenthesis.counter < 2:  # type: ignore
        raise RetryException("Simulated failure")


@reattempt()
def retry_function_with_parenthesis():
    retry_function_with_parenthesis.counter += 1  # type: ignore
    if retry_function_with_parenthesis.counter < 2:  # type: ignore
        raise RetryException("Simulated failure")


@reattempt(max_retries=1)
def retry_function_with_max_retries():
    retry_function_with_max_retries.counter += 1  # type: ignore
    if retry_function_with_max_retries.counter < 2:  # type: ignore
        raise RetryException("Simulated failure")


@reattempt(min_time=0.1)
def retry_function_with_min_time():
    retry_function_with_min_time.counter += 1  # type: ignore
    if retry_function_with_min_time.counter < 2:  # type: ignore
        raise RetryException("Simulated failure")


@reattempt(max_time=1.0)
def retry_function_with_max_time():
    retry_function_with_max_time.counter += 1  # type: ignore
    if retry_function_with_max_time.counter < 2:  # type: ignore
        raise RetryException("Simulated failure")


@reattempt(max_retries=2, min_time=0.2, max_time=2.0)
def retry_function_with_all_params():
    retry_function_with_all_params.counter += 1  # type: ignore
    if retry_function_with_all_params.counter < 2:  # type: ignore
        raise RetryException("Simulated failure")


@pytest.mark.asyncio
async def test_retry_function_without_parenthesis(disable_logging_exception):
    retry_function_without_parenthesis.counter = 0  # type: ignore
    retry_function_without_parenthesis()
    assert retry_function_without_parenthesis.counter == 2  # type: ignore


@pytest.mark.asyncio
async def test_retry_function_with_parenthesis(disable_logging_exception):
    retry_function_with_parenthesis.counter = 0  # type: ignore
    retry_function_with_parenthesis()
    assert retry_function_with_parenthesis.counter == 2  # type: ignore


@pytest.mark.asyncio
async def test_retry_function_with_max_retries(disable_logging_exception):
    retry_function_with_max_retries.counter = 0  # type: ignore
    with pytest.raises(RetryException):
        retry_function_with_max_retries()
    assert retry_function_with_max_retries.counter == 1  # type: ignore


@pytest.mark.asyncio
async def test_retry_function_with_min_time(disable_logging_exception):
    retry_function_with_min_time.counter = 0  # type: ignore
    retry_function_with_min_time()
    assert retry_function_with_min_time.counter == 2  # type: ignore


@pytest.mark.asyncio
async def test_retry_function_with_max_time(disable_logging_exception):
    retry_function_with_max_time.counter = 0  # type: ignore
    retry_function_with_max_time()
    assert retry_function_with_max_time.counter == 2  # type: ignore


@pytest.mark.asyncio
async def test_retry_function_with_all_params(disable_logging_exception):
    retry_function_with_all_params.counter = 0  # type: ignore
    retry_function_with_all_params()
    assert retry_function_with_all_params.counter == 2  # type: ignore
