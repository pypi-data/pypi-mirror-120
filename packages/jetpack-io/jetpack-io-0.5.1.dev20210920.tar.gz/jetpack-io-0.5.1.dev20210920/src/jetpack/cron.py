import os
from typing import Any, Callable

import cronitor
import schedule
from schedule import every  # Use this to whitelist what we allow

from jetpack import utils

cronjob_suffix = os.environ.get("JETPACK_CRONJOB_SUFFIX", "-missing-suffix")


def repeat(repeat_pattern: schedule.Job) -> Callable[..., Any]:
    def wrapper(func: Callable[..., Any]) -> Any:
        job_name = utils.qualified_func_name(func) + cronjob_suffix
        cronitor_wrapped_func = cronitor.job(job_name)(func)
        return schedule.repeat(repeat_pattern)(cronitor_wrapped_func)

    return wrapper
