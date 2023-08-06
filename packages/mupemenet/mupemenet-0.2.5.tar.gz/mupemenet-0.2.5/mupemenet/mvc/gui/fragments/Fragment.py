from abc import abstractmethod
from typing import Any
from mupemenet.mvc.views.View import View
from mupemenet.mvc.controllers.Controller import Controller
from tkinter import *

from mupemenet.mvc.models.Model import Model


class Fragment:
    """
    fragment introduce modularity and re-usability by allowing the main UI to be
    divided into discrete chunks. Following method are to be implemented:
    - create_view: Process of creating the view
    - on_view_created: Action to perform when the view har been created and attached 
        to the root UI
    - update_model: Action to perform when model is being manipulated 
    - update_view: Action to perform when the view is being updated
    
    Inspired by Android fragments. 
    https://developer.android.com/guide/fragments
    """

    def __init__(self, TAG: str, model: Model, view: View, controller: Controller=Controller(), params: Any=None) -> None:
        self.params = params
        self.TAG = TAG
        self.__model__ = model
        self.__view__ = view
        self.__controller__ = controller

    def get_tag(self):
        return self.TAG

    
    def on_create_view(self, master: Frame) -> None:
        self.__view__.create_view(master=master)

    @abstractmethod
    def on_view_created(self) -> None:
        pass

    def get_root(self):
        return self.root

    def add(self, root: Tk):
        self.root = root
        self.frame = frame = Frame(master=self.root)
        frame.pack(expand=True)
        self.on_create_view(master=self.frame)
        self.bind()
        self.on_view_created()

    def remove(self):
        """
        Removes the fragment. Could be overwritten if one wants to perform some housekeeping before
        TODO - Implements exception if super is not called when overwritten
        """
        self.frame.destroy()

    def get_root_size(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        return width, height

    def bind(self):
        self.get_controller().bind(self.__model__, self.__view__)

    def get_controller(self):
        return self.__controller__
