# -*- coding: utf-8 -*-
from mupemenet.facerecognitionpipeline.Enhancer import Enhancer
from logging import debug, warning
from mupemenet.mvc.eventbus.BasicEvents import *
from mupemenet.mvc.utils.Utils import *
from tkinter import BOTH, Frame, Label
from PIL import Image, ImageTk
import cv2
from timeit import default_timer as timer
import asyncio
from pyeventbus3.pyeventbus3 import PyBus
from mupemenet.mvc.gui.fragments.Fragment import Fragment
from mupemenet.mvc.views.View import View
from mupemenet.mvc.models.PipelineModel import PipelineModel, Ranger


class PipelineFragment(Fragment, View):

    def __init__(self, TAG, user_result_callback=None, extra_params=None):
        model = PipelineModel()
        super().__init__(TAG, model=model, view=self)
        debug("Registering PipelineModel() class to eventbus")
        self.user_result_callback = user_result_callback
        self.extra_params = extra_params
        cap = self.cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 960)
        self.tof = Ranger()
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        debug(f"Frame rate: {fps} fps")
        self.wait_ms = round( 1000 / fps)
        self.enhancer = Enhancer()
        
        
    def create_view(self, master: Frame) -> None:
        self.frame_container = Label(master=master)
        self.frame_container.pack(fill=BOTH)
        self.info_container = Label(master=master, borderwidth=1, relief="solid")
        self.info_container.config(font=('Helvatical bold', 24))
        self.info_container.place(relx=1.0, rely=1.0, x=-2, y=-2, anchor="se")

    def on_view_created(self) -> None:
        grabbed_frames = list()
        self.capture(timer(), timer(), self.get_root_size(), grabbed_frames)
        
    def run_callable(self, user):
        if self.user_result_callback is None:
            return
        self.user_result_callback(user, self.extra_params)
            


    def capture(self, capture_time, timeout_time, dsize, grabbed_frames):
        count_down = max(15 - delta_s(timeout_time), 0)
        if count_down<=0:
            warning("Timeout occured")
            user = no_user()
            user['message'] = 'timeout'
            self.run_callable(user)                
            PyBus.Instance().post(CaptureTimeout())   
            return
        if delta_ms(capture_time)>=3000 and len(grabbed_frames)>=20:
            debug(f"Image capture done. Grabbed {len(grabbed_frames)}")
            self.get_controller().fire(update_obj=grabbed_frames)
            return
        _, frame = self.cap.read()
        frame = self.enhancer.enhance(frame)
        distance = self.tof.get_distance()
        if self.tof.is_within_range(distance):
            tof_message = "DISTANCE OK"
            color = COLOR_GREEN_BGR
            grabbed_frames.append(frame.copy())
        else:
            capture_time = timer()
            grabbed_frames.clear()
            if self.tof.is_too_close(distance=distance):
                tof_message = "Eloignez-vous un peu de l'appareil"
                color = COLOR_YELLOW_BGR
            elif self.tof.is_too_far(distance=distance):
                color = COLOR_RED_BGR
                tof_message = "Rapprochez-vous un peu de l'appareil"

        font = cv2.FONT_HERSHEY_DUPLEX
        fontScale = 1
        thickness = 2
        textsize = cv2.getTextSize(tof_message, font, fontScale, thickness)[0]     
        textX = (frame.shape[1] - textsize[0]) // 2
        textY = (frame.shape[0] + textsize[1]) // 2  
        cv2.putText(frame, tof_message, (textX, 24), font, fontScale, color, thickness)
        frame = cv2.resize(frame, dsize=dsize)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.frame_container.image = image
        self.frame_container.configure(image=image)
        self.frame_container.after(self.wait_ms, self.capture, capture_time, timeout_time, dsize, grabbed_frames)    


    def display_user_info(self, user):
        debug(f"User: {user}")
        self.info_container.configure(text=f"{user['matricule']}\n{user['name']}", 
        background = 'red' if user['id']<0 else 'green')
        self.run_callable(user)


    def update_view(self, update_obj):
        self.display_user_info(update_obj)
        self.info_container.bind("<Button-1>", lambda event: PyBus.Instance().post(StandByEvent()))

        def flash(count_time):
            if delta_s(count_time)>=10:
                PyBus.Instance().post(StandByEvent())
                return
            bg = self.info_container.cget("background")
            fg = self.info_container.cget("foreground")
            self.info_container.configure(background=fg, foreground=bg)
            self.info_container.after(500, flash, count_time)
        
        flash(timer())

    # House keeping
    def remove(self):
        debug(f"House keeping in {self.__class__.__name__}")
        self.tof.close()
        self.cap.release()
        super().remove()
