from typing import Any, Callable

from jetpack._job.job import Job as _Job


class JobDecorator:
    def __call__(self, fn: Callable[..., Any]) -> Callable[..., Any]:
        return _Job(fn)


job = JobDecorator()
