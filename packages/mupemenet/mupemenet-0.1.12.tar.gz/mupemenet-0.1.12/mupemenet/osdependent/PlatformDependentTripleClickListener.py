from abc import ABC, abstractmethod
from mupemenet.mvc.eventbus.BasicEvents import FrPipelineRequest

from pyeventbus3.pyeventbus3 import PyBus


class PlatformDependentTripleClickListener(ABC):

    @abstractmethod
    def enter(self, params=None):
        raise NotImplemented

    @abstractmethod
    def exit(self):
        raise NotImplemented

    @staticmethod
    def triple_button_click_action(event):
        PyBus.Instance().post(FrPipelineRequest())
