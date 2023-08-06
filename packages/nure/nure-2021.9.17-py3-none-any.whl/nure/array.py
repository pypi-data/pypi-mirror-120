import concurrent.futures
import os
from collections import Iterable, deque
from typing import Callable

_DEFAULT_N_WORKERS_ = os.cpu_count() or 4


def parallelize_iterable(iterable: Iterable, func: Callable, *args, retain_order=True,
                         executor: concurrent.futures.Executor = None,
                         n_workers: int = _DEFAULT_N_WORKERS_, use_process: bool = False,
                         **kwargs):
    # check if exe is provided
    if executor is None:
        if use_process:
            my_executor = concurrent.futures.ProcessPoolExecutor(max_workers=n_workers)
        else:
            my_executor = concurrent.futures.ThreadPoolExecutor(max_workers=n_workers)
    else:
        my_executor = executor

    # submit tasks
    task_list = deque([my_executor.submit(func, item, *args, **kwargs) for item in iterable])

    # collect results
    # note to remove completed task from the list for memory efficiency
    for task in concurrent.futures.as_completed(task_list):
        if retain_order:
            while len(task_list) > 0 and task_list[0].done():
                yield task_list.popleft().result()
        else:
            task_list.remove(task)
            yield task.result()

            # if is my exe, then shutdown
    if executor is None:
        my_executor.shutdown()
