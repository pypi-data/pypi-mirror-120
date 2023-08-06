from mupemenet.mvc.models.Model import Model
from tkinter import PhotoImage

class StandByModel(Model):

    def update(self):
        self.update_listener('/home/pi/mupemenet/resources/kelwe2.png')
        
