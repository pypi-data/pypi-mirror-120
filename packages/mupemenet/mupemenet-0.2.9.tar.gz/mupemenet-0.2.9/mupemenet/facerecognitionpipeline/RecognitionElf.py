from logging import debug
from mupemenet.userdb.UserDB import UserDB

import cv2
import cv2.ml
import numpy as np

from mupemenet.config.Config import Config
from mupemenet.facenet.Facenet import Facenet
from mupemenet.mvc.utils.Utils import mupemenet_singleton, measure, no_user


def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    # x = n/np.sum(n)
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


@mupemenet_singleton
class RecognitionElf:

    def __init__(self) -> None:
        self.facenet = Facenet()
        self.frdb = cv2.ml.KNearest_load(Config.MODELS_PATH + "/faces.xml")
        self.db = UserDB()

    def histeq(self, img):
        ycrcb_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        # equalize the histogram of the Y channel
        ycrcb_img[:, :, 0] = cv2.equalizeHist(ycrcb_img[:, :, 0])

        # convert back to RGB color-space from YCrCb
        equalized_img = cv2.cvtColor(ycrcb_img, cv2.COLOR_YCrCb2BGR)
        return equalized_img


    def embed(self, img):
        return self.facenet.infer(img)

    def classify(self, embeddings):
        return self.frdb.findNearest(embeddings, 5)

    def recognize(self, img):
        if img is None:
            return no_user()
        img = self.histeq(img=img)
        embeddings = self.embed(img)
        ret, _, neighbours, dist = self.classify(embeddings)
        s = len(set(neighbours[0].tolist()))
        avg_dst = np.mean(dist[0])
        debug(f'\nneighbs. {neighbours}\ndist. {dist}\navg_dist. {avg_dst}')
        if s==1 and avg_dst<0.65: # Perfect match
            id = int(ret)
            user = self.db.get_user_by_id(id)
            user['message'] = "sucess"
            return user
        return no_user()


