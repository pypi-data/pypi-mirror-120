from tkinter import Entry

import mupemenet.osdependent
from mupemenet.osdependent.platforms import platform_dependent


@platform_dependent(win=mupemenet.osdependent.windows.EditView, rpi=mupemenet.osdependent.raspberrypios.EditView)
class EditView(Entry):
    pass
