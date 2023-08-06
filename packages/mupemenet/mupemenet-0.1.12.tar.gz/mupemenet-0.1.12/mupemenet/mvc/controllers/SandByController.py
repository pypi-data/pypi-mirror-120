from mupemenet.mvc.models.Model import Model
from mupemenet.mvc.views.View import View
from mupemenet.mvc.controllers.Controller import Controller
from mupemenet.mvc.views.StandByView import StandByView
from mupemenet.mvc.models.StandByModel import StandByModel

class StandByController(Controller):
  
    def init_view(self, master) -> View:
        return StandByView(master=master)

    def init_model(self) -> Model:
        return StandByModel()

    def on_model_update(self, update_obj):
        self.view.update_view(update_obj)
