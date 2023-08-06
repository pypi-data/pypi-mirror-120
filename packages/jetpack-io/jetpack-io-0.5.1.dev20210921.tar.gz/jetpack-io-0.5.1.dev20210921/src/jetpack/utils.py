from typing import Any, Callable

import schedule


def job_name(job: schedule.Job) -> str:
    return qualified_func_name(job.job_func.func)


def qualified_func_name(func: Callable[..., Any]) -> str:
    return f"{func.__module__}.{func.__name__}"
