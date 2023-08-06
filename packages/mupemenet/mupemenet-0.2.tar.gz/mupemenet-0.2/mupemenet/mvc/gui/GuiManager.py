from mupemenet.services.Jobs import Jobs
from mupemenet.services.Servers import FaceRecognitionServer, launch_face_recognition_servers
from mupemenet.facerecognitionpipeline.PipelineFragment import PipelineFragment
from tkinter import *
from typing import Union

from pyeventbus3.pyeventbus3 import *

from mupemenet.mvc.eventbus.MupemenetBus import MupemenetBus
from mupemenet.mvc.gui.fragments.DataFetchingFragment import DataFetchingFragment
from mupemenet.mvc.gui.fragments.Fragment import Fragment
from mupemenet.osdependent.platforms import platform_dependent


def fc_win(ui_root):
    ui_root.geometry('800x480')


def fc_rpi(ui_root):
    ui_root.attributes('-fullscreen', True)


@platform_dependent(win=fc_win, rpi=fc_rpi)
def full_screen(ui_root):
    pass


class GuiManager:

    def __init__(self) -> None:
        Jobs()
        global ui_root
        ui_root = Tk()
        self.last_fragment: Union[Fragment, None] = None
        full_screen(ui_root)
        self.mupemenet_bus = mupemenet_bus = MupemenetBus(ui_root)
        mupemenet_bus.register(mupemenet_bus)



    def run(self):
        self.mupemenet_bus.set_fragment(DataFetchingFragment("DataFetchingFragment"))
        ui_root.mainloop()
