from datetime import datetime
import json
from mupemenet.mvc.views.DataFetchingView import DataFetchingView
from mupemenet.mvc.models.DataFetchingModel import DataFetchingModel
from tkinter import *
from tkinter.ttk import *

from mupemenet.mvc.gui.fragments.Fragment import Fragment


class DataFetchingFragment(Fragment):

    def __init__(self, TAG: str) -> None:
        super().__init__(TAG, model=DataFetchingModel(), view=DataFetchingView())
        

    def on_view_created(self) -> None:
        self.get_controller().fire(None)
    
