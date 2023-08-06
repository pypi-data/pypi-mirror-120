import tkinter as tk
from tkinter.constants import BOTH
from typing import Tuple
from PIL import Image, ImageTk
from mupemenet.mvc.views.View import View

class StandByView(View):

    def __init__(self, ui_root_size: Tuple[int, int]) -> None:
        super().__init__()
        self.ui_root_size = ui_root_size

    def update_view(self, update_obj):
        load = Image.open(update_obj).resize(self.ui_root_size, Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(master=self.widget, image=render)
        img.image = render
        img.pack(fill=BOTH,  expand=True)