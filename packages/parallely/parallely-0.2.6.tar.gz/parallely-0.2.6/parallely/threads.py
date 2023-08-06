from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from multiprocessing import cpu_count
from typing import Any, Callable, List, Optional

from parallely.base import ParalellyFunction
from parallely.utils import prepare_arguments


class ThreadedFunction(ParalellyFunction):
    def __init__(self, func: Callable, max_workers: int, batch_size: Optional[int]):
        super().__init__(func, max_workers)
        self._batch_size = batch_size

    def _execute_once(self, *args, **kwargs) -> Any:
        return self._func(*args, **kwargs)

    def map(self, *args, **kwargs) -> List[Any]:
        return list(self.imap(*args, **kwargs))

    def imap(self, *args, **kwargs) -> List[Any]:
        args, kwargs = prepare_arguments(args, kwargs)
        pool_size = min(self._max_workers, len(args))

        with ThreadPoolExecutor(pool_size) as pool:
            for b_args, b_kwargs in zip(self._batch(args, steps=self._batch_size), self._batch(kwargs, steps=self._batch_size)):
                futures = [pool.submit(self._execute_once, *arg, **kwarg) for arg, kwarg in zip(b_args, b_kwargs)]
                for future in futures:
                    yield future.result() 

    def acmap(self, *args, **kwargs) -> List[Any]:
        args, kwargs = prepare_arguments(args, kwargs)
        pool_size = min(self._max_workers, len(args))

        with ThreadPoolExecutor(pool_size) as pool:
            for b_args, b_kwargs in zip(self._batch(args, steps=self._batch_size), self._batch(kwargs, steps=self._batch_size)):
                for future in as_completed([pool.submit(self._execute_once, *arg, **kwarg) for arg, kwarg in zip(b_args, b_kwargs)]):
                    yield future.result()

def threaded(func: Callable = None, max_workers: Optional[int] = None, batch_size: Optional[int] = None) -> ThreadedFunction:
    """

    :param func:
    :param max_workers:
    :return:
    """

    max_workers = max_workers if max_workers is not None else cpu_count() * 10
    batch_size =  batch_size if batch_size is not None else  4 * max_workers

    if func is None:
        return partial(threaded, max_workers=max_workers, batch_size=batch_size)

    return ThreadedFunction(func, max_workers, batch_size)
