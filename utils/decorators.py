import time
import functools
import logging

logger = logging.getLogger('web_automation')


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.time() - start
            logger.info(f"{func.__name__} levou {elapsed:.2f}s")
    return wrapper


def retry_on_fail(retries: int = 3, delay: float = 1.0):
    def deco(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            last_exc = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger.warning(f"Tentativa {attempt}/{retries} falhou: {e}")
                    time.sleep(delay)
            raise last_exc
        return wrapped
    return deco