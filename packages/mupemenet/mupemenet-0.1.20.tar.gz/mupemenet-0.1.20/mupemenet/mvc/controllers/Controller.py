from mupemenet.mvc.exceptions.Customexceptions import *
from mupemenet.mvc.models.Model import Model
from mupemenet.mvc.views.View import View


class Controller:

    def bind(self, model: Model, view: View):
        self.__model__ = model
        self.__view__ = view
        self.__model__.set_update_listener(self.on_model_update)

    def on_model_update(self, update_obj):
        self.__view__.update_view(update_obj=update_obj)

    def get_view(self):
        return self.__view__
    
    def get_model(self):
        return self.__model__

    def fire(self, update_obj):
        self.__model__.update_model(update_obj=update_obj)
