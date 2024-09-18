import time
from typing import Callable

from wrapper_geocode_reverse.src.core import logger

logger = logger.getLogger(__name__)


def measure_time(func: Callable):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        func_info = f'Function "{func.__name__}"'
        time_info = f'executed in {execution_time:.6f} seconds'
        info = f'{func_info}: {time_info}'
        logger.info(info)
        return result
    return wrapper
