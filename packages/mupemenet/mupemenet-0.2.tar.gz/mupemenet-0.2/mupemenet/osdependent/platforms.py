import platform
from functools import wraps


def platform_dependent(win, rpi):
    def decorator(cls):
        def wrapper(*args, **kwargs):
            if platform.system().lower().startswith('win'):
                cls = win
            elif platform.system().lower().startswith('lin'):
                cls = rpi
            else:
                raise RuntimeError("Platform implementation not supported")
            return cls(*args, **kwargs)

        return wrapper

    return decorator


def platform_is():
    return platform.system().lower()[:3]
