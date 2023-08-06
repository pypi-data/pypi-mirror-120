from logging import debug
from threading import RLock
from timeit import default_timer as timer
from math import ceil
import subprocess
import sys


COLOR_RED_BGR = (0, 0, 255)
COLOR_GREEN_BGR = (0, 255, 0)
COLOR_YELLOW_BGR = (0, 255, 255)

MIN_TOF_RANGE = 30
MAX_TOF_RANGE = 70
MIN_BB_IMAGE_RATIO = 0.3

"""
Code taken from 
https://betterprogramming.pub/singleton-in-python-5eaa66618e3d
"""
def mupemenet_singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


def measure(func):
    def decorator(*args, **kwargs):
        t = timer()
        ret_fun = func(*args, **kwargs)
        t = timer() - t
        if t >= 1:
            t0 = ceil(t)
            unit = 's'
        else:
            t0 = ceil(1000 * t)
            unit = 'ms'
        debug("Method: {} took {} {}".format(func.__name__, t0, unit))
        return ret_fun

    return decorator


def synchronized(func):
    def decorator(*args, **kwargs):
        with RLock():
            return func(*args, **kwargs)
    return decorator




def no_user():
        return  {
            "matricule": "XXXXXXX",
            "name": "INCONNU(E)",
            "id": -1,
            "message": "Unknown"
        }

def is_exit_signal(inp):
    return isinstance(inp, str) and inp.upper()=='EXIT'

def delta_ms(previous_t):
           t = timer() - previous_t
           return ceil(1000 * t)

def delta_s(previous_t):
    t = timer() - previous_t
    return ceil(t)


def check(name='mupemenet'):
    """
    Check the latest version of 
    """
    latest_version = str(subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '{}==random'.format(name)], 
        capture_output=True, text=True))

    latest_version = latest_version[latest_version.find('(from versions:')+15:]
    latest_version = latest_version[:latest_version.find(')')]
    latest_version = latest_version.replace(' ','').split(',')[-1]

    current_version = str(subprocess.run(
        [sys.executable, '-m', 'pip', 'show', '{}'.format(name)], 
        capture_output=True, text=True))
    current_version = current_version[current_version.find('Version:')+8:]
    current_version = current_version[:current_version.find('\\n')].replace(' ','') 

    if latest_version == current_version:
        return True
    else:
        return False

