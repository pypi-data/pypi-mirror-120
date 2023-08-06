from mupemenet.mvc.utils.Utils import measure, mupemenet_singleton
from mupemenet.BlazeFaceDetection.blazeFaceDetector import blazeFaceDetector


@mupemenet_singleton
class DetectionElf:

    def __init__(self):
        self.detector = blazeFaceDetector('front')

    def detect(self, img) -> list:
        bboxes = list()
        if img is None:
            return bboxes
        def refine(x1, y1, x2, y2) -> tuple:
            h = y2 - y1
            y1_r = max(y1 - h // 3, 0)
            w = x2 - x1
            w_percent = 10*w/100
            x1_r, x2_r = int(x1+w_percent), int(x2-w_percent)
            return x1_r, y1_r, x2_r - x1_r, y2 - y1_r

        img_height, img_width, _ = img.shape
        results = self.detector.detectFaces(img)
        boundingBoxes = results.boxes
        for boundingBox in boundingBoxes:
            x1 = (img_width * boundingBox[0]).astype(int)
            x2 = (img_width * boundingBox[2]).astype(int)
            y1 = (img_height * boundingBox[1]).astype(int)
            y2 = (img_height * boundingBox[3]).astype(int)
            r = refine(x1, y1, x2, y2)
            bboxes.append(r)
        return bboxes
