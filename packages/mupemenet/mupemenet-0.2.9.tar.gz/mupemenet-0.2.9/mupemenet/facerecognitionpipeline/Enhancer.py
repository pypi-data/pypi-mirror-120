from logging import debug, error
from mupemenet.config.Config import Config
from mupemenet.mvc.utils.Utils import measure
import cv2
import numpy as np
from numpy.ma import mean

class Enhancer:

    def __init__(self):
        path = Config.MODELS_PATH + "/ctbr_enhancer_dtree.xml"
        self.mdl = cv2.ml.DTrees_load(path)
        self.ctbr_dict = self.label2ctbr()

    def apply(self, rgb_img, contrast, brightness):
        return cv2.addWeighted(rgb_img, contrast, rgb_img, 0, brightness)

    @measure
    def enhance(self, frame):
        ct, br = self.estimate(frame)
        inp = np.float32(np.array([ct, br]).reshape((1, 2)))
        resp = self.mdl.predict(inp)[0]
        e_ct, e_br = self.ctbr_dict[int(resp)]
        debug(f"Enhancer: {ct}/{br} -> {e_ct}/{e_br}")
        enhanced_frame = self.apply(frame, e_ct, e_br)
        return enhanced_frame


    def estimate(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ii = cv2.integral(gray)
        height, width = ii.shape
        w, h = width//2, height//2
        tl, tr, bl, br, md = (0, 0, w, h), (w, 0, w, h), (0, h, w, h), (w, h, w, h), (w//2, h//2, w, h)
        coords = [tl, tr, bl, br, md]
        lst = []
        for c in coords:
            lst += [self.mean_from_ii(ii, c[0], c[1], c[2], c[3])]
        minVal, maxVal = min(lst), max(lst)
        return round(maxVal - minVal), round(mean(lst))

    @staticmethod
    def mean_from_ii(ii, x, y, w, h):
        tl, br, tr, bl = ii[y, x], ii[y + h, x + w], ii[y, x + w], ii[y + h, x]
        return (br + tl - tr - bl) / (w * h)

    @staticmethod
    def label2ctbr():
        ctbr = dict()
        ctbr[0] = (1, 0)
        ctbr[1] = (2, 12)
        ctbr[2] = (2, 24)
        ctbr[3] = (2, 84)
        ctbr[4] = (2, 120)
        ctbr[5] = (4, 24)
        ctbr[6] = (4, 48)
        ctbr[7] = (4, 60)
        ctbr[8] = (4, 96)
        ctbr[9] = (6, 12)
        ctbr[10] = (6, 48)
        ctbr[11] = (8, 36)
        return ctbr