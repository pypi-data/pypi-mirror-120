from mupemenet.config.Config import Config
from mupemenet.mvc.views.View import View
from tkinter import Frame, Label
from tkinter import Frame, Label
from tkinter.constants import BOTH

from PIL import Image, ImageTk
from mupemenet.mvc.models.Model import Model

import mupemenet.osdependent
from mupemenet.mvc.gui.fragments.Fragment import Fragment
from mupemenet.osdependent.PlatformDependentTripleClickListener import PlatformDependentTripleClickListener
from mupemenet.osdependent.platforms import platform_dependent
from mupemenet.osdependent.raspberrypios.RpiTripleClickListener import RpiTripleClickListener
from mupemenet.osdependent.windows.WinTripleClickListener import WinTripleClickListener


@platform_dependent(
    rpi=mupemenet.osdependent.raspberrypios.RpiTripleClickListener.RpiTripleClickListener,
    win=mupemenet.osdependent.windows.WinTripleClickListener.WinTripleClickListener
)
class TripleClickHandler(PlatformDependentTripleClickListener):
    def enter(self, params=None):
        pass

    def exit(self):
        pass


class StandByFragment(Fragment, Model, View):

    def __init__(self, TAG: str):
        super().__init__(TAG, model=self, view=self)
        self.triple_click_handler = TripleClickHandler()

    def create_view(self, master):
        self.view = Frame(master=master)
        self.view.pack(fill=BOTH)


    def on_view_created(self) -> None:
        self.get_controller().fire(None)

    def update_model(self, update_obj):
        filename = Config.RESOURCES_PATH + '/kelwe2.png'
        load = Image.open(filename).resize(self.get_root_size(), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        self.label = label = Label(master=self.view, image=render)
        label.image = render
        self.update_listener(None)

    def remove(self):
        # Housekeeping goes here
        self.triple_click_handler.exit()
        super().remove()

    def update_view(self, update_obj):
        self.label.pack(fill=BOTH, expand=True)
        self.triple_click_handler.enter(self.label)

