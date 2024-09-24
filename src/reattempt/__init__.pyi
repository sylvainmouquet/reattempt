from typing import Callable, TypeVar, Union, Awaitable

T = TypeVar('T')

def reattempt(
    max_retries: int,
    min_time: float,
    max_time: float
) -> Callable[[Callable[..., Union[T, Awaitable[T]]]], Callable[..., Union[T, Awaitable[T]]]]:
    ...
