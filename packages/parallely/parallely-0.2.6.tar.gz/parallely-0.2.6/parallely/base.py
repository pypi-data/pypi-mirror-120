from typing import Any, Callable, List


class ParalellyFunction:
    def __init__(self, func: Callable, max_workers: int):

        self._func = func
        self._max_workers = max_workers

    def map(self, *args, **kwargs) -> List[Any]:
        raise NotImplementedError("All children should implement map")

    def _batch(self, batch_size, args, kwargs):
        if len(args) <= batch_size:
            return args, kwargs

    def _batch(self, elements, groups=None, steps=None):
        def batch(elements, n):
            for i, index in enumerate(range(0, len(elements), n)):
                yield elements[index : index + n] if i != n else elements[index:]

        if groups is None and steps is None:
            raise(ValueError(groups, steps))

        n = steps if steps else len(elements) // groups

        if len(elements) < n:
            return [elements]
        else:
            return list(batch(elements, n))

    def _execute_once(self, *args, **kwargs) -> Any:
        raise NotImplementedError()

    def __call__(self, *args, **kwargs) -> Any:
        return self._execute_once(*args, **kwargs)
