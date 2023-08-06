from logging import debug
from mupemenet.services.Servers import launch_face_recognition_servers
from mupemenet.mvc.eventbus.BasicEvents import *
from typing import Union

from pyeventbus3.pyeventbus3 import PyBus, subscribe, Mode

from mupemenet.facerecognitionpipeline.PipelineFragment import PipelineFragment
from mupemenet.mvc.eventbus.BasicEvents import *
from mupemenet.mvc.gui.fragments.Fragment import Fragment
from mupemenet.mvc.gui.fragments.StandbyFragment import StandByFragment
from mupemenet.mvc.utils.Utils import mupemenet_singleton


@mupemenet_singleton
class MupemenetBus:

    def __init__(self, ui_root):
        self.ui_root = ui_root
        self.last_fragment: Union[Fragment, None] = None

    def register(self, myclass):
        PyBus.Instance().register(myclass, self.__class__.__name__)

    def set_fragment(self, fragment: Fragment):
        if self.last_fragment is not None:
            self.last_fragment.remove()
        self.last_fragment = fragment
        fragment.add(self.ui_root)

    @subscribe(onEvent=DataFetched)
    def on_data_fetched(self, event):
        debug("Data fetched. Entering idle mode")
        self.set_fragment(StandByFragment("StandByFragment"))
        launch_face_recognition_servers()

    @subscribe(onEvent=FrPipelineRequest, threadMode=Mode.BACKGROUND)
    def on_data_fetched(self, event: FrPipelineRequest):
        debug("FR pipeline triggered")
        pipeline_fragment = PipelineFragment("fr_pipeline", event.user_result_callback, event.extra_params)
        self.set_fragment(pipeline_fragment)

    @subscribe(onEvent=CaptureTimeout)
    def on_capture_timeout(self, event):
        self.set_fragment(StandByFragment("StandByFragment"))

    @subscribe(onEvent=StandByEvent)
    def on_capture_timeout(self, event):
        self.set_fragment(StandByFragment("StandByFragment"))

    
