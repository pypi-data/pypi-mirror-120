from mupemenet.mvc.eventbus.BasicEvents import DataFetched
from mupemenet.mvc.views.View import View
from tkinter import Label, StringVar
from tkinter.constants import HORIZONTAL
from tkinter.ttk import Progressbar
from pyeventbus3.pyeventbus3 import PyBus

class DataFetchingView(View):
    
    def create_view(self, master):
        Label(master=master).grid(row=0, column=1)
        self.data_fetching_message = StringVar()
        self.lb = lb = Label(
            master=master,
            textvariable=self.data_fetching_message
        )
        self.data_fetching_message.set("Téléchargement de données. Veuillez patienter...")
        lb.grid(row=1, column=1)
        self.pb = pb = Progressbar(master=master, orient=HORIZONTAL, length=200, mode='indeterminate')
        pb.grid(row=2, column=1)
        pb.start()

    

    def update_view(self, update_obj):
        self.pb.stop()
        self.lb.config(background=update_obj['message_color'])
        self.data_fetching_message.set(update_obj['message'])
        PyBus.Instance().post(DataFetched())