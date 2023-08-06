from abc import ABC, abstractmethod
from logging import debug
from queue import Queue
from threading import Thread

from numpy import equal
from mupemenet.facerecognitionpipeline.RecognitionElf import RecognitionElf
from mupemenet.facerecognitionpipeline.DetectionElf import DetectionElf

from mupemenet.mvc.models.Model import Model
from mupemenet.mvc.utils.Utils import MAX_TOF_RANGE, MIN_BB_IMAGE_RATIO, MIN_TOF_RANGE, is_exit_signal, measure, no_user
from mupemenet.osdependent.platforms import platform_dependent
from multiprocessing import Process

class OsRanger(ABC):

    @abstractmethod
    def get_distance(self) -> int:
        raise NotImplemented

    @abstractmethod
    def close(self):
        raise NotImplemented

    def is_within_range(self, distance):
        return MIN_TOF_RANGE < distance < MAX_TOF_RANGE

    def is_too_close(self, distance):
        return distance <= MIN_TOF_RANGE

    def is_too_far(self, distance):
        return distance >= MAX_TOF_RANGE


class WinRanger(OsRanger):
    def get_distance(self) -> int:
        return 60

    def close(self):
        pass


class RpiRanger(OsRanger):
    def __init__(self) -> None:
        import mupemenet.VL53L0X_rasp_python.python.VL53L0X as VL
        self.tof = VL.VL53L0X()
        self.tof.start_ranging(VL.VL53L0X_BETTER_ACCURACY_MODE)

    def get_distance(self) -> int:
        return self.tof.get_distance() // 10

    def close(self):
        self.tof.stop_ranging()


@platform_dependent(win=WinRanger, rpi=RpiRanger)
class Ranger(OsRanger):
    pass


class PipelineModel(Model):

    def __init__(self) -> None:
        super().__init__()
        self.detector = DetectionElf()
        self.recognizer = RecognitionElf()
    
    def update_model(self, update_obj):
        grabbed_frames = update_obj

        def prune_frames(grabbed_frames):
            pruned = list()
            l = len(grabbed_frames)
            pruned.append(grabbed_frames[l//4])
            pruned.append(grabbed_frames[l//2])
            pruned.append(grabbed_frames[3*l//4])
            return pruned

        @measure
        def run(frame):
            bboxes  = self.detector.detect(frame)
            cropped = None
            if bboxes:
                sorted(bboxes, key=lambda box: box[2] * box[3], reverse=True)
                x, y, w, h = bboxes[0]
                x1, y1, x2, y2 = x, y, x+w, y+h
                img_height, img_width, _ = frame.shape
                ratio = (h)/(img_height)
                if ratio >= MIN_BB_IMAGE_RATIO:
                    cropped = frame[y1:y2, x1:x2]
                debug(f'{len(bboxes)} faces detectées. Ratio: {ratio}')
            user = self.recognizer.recognize(cropped)
            return user

        pruned = prune_frames(grabbed_frames)
        user = no_user()
        for frame in pruned:
            user = run(frame)
            if user['id']>=0:
                break
        self.update_listener(user)

        
        


