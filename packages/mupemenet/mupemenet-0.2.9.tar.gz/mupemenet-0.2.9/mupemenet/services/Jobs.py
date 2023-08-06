from logging import debug, error
import subprocess
import sys, os
from threading import Thread
from multiprocessing import Process
from schedule import every, repeat, run_pending
from mupemenet.mvc.utils.Utils import has_update, mupemenet_singleton
import importlib

@repeat(every(30).days)
def fetch_new_users():
    '''
    TODO - Implement fetching new users periodically by decoupling 
    update_model from DataFetchingFragment
    '''
    pass


def install(package='mupemenet'):
    try:
        debug(f'Installing package {package}')
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])
        debug(f"Package {package} sucessfully installed")
    except Exception as e:
        error(f'Failed to install {package}. Cause: {e}')


def package_exist(package):
    spam_spec = importlib.util.find_spec(package)
    found = spam_spec is not None
    return found


# @repeat(every().day.at("12:00"))
@repeat(every().minute)
def update_manager():
    new_version = has_update()
    if new_version: 
        debug("New version is available")
        install()
        debug("Rebooting")
        os.system("sudo reboot")
    else:
        debug("Software is up-to-date")



@mupemenet_singleton
class Jobs:
    '''
    Runs jobs declared jobs in Job.py
    '''
    def __init__(self) -> None:
        
        def __fire__():
            while True:
                run_pending()

        job_queue = Process(target=__fire__, daemon=True)
        job_queue.start()
        

