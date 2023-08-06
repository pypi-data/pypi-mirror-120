import logging
import coloredlogs
from mupemenet.config.Config import config_env
import os
from mupemenet.mvc.gui.GuiManager import GuiManager
from mupemenet.osdependent.platforms import platform_dependent

def init_app_on_win():
    pass


def init_app_on_rpi():
    if os.environ.get('DISPLAY', '') == '':
        os.environ.__setitem__('DISPLAY', ':0.0')
        # subprocess.Popen("florence")


@platform_dependent(win=init_app_on_win, rpi=init_app_on_rpi)
def init_app():
    pass


def main():
    init_app()
    coloredlogs.install(level='DEBUG')
    logging.getLogger().setLevel(level=logging.DEBUG)
    config_env(env='debug')
    GuiManager().run()


if __name__ == '__main__':
    # main()
    import sys,os
    print(f"dir: {os.path.realpath('.')}")
