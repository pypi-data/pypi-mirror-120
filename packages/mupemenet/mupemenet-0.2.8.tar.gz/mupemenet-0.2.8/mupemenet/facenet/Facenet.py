import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter

from mupemenet.config.Config import Config
from mupemenet.mvc.utils.Utils import measure


class Facenet:
    def __init__(self) -> None:
        self.interpreter = Interpreter(model_path=Config.MODELS_PATH+"/facenet_int8.tflite", num_threads=4)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        input_shape = self.input_details[0]['shape']
        self.inputHeight = input_shape[1]
        self.inputWidth = input_shape[2]
        self.channels = input_shape[3]

    def infer(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img, (self.inputHeight, self.inputWidth), interpolation=cv2.INTER_CUBIC) / 255.0
        # Adjust matrix dimenstions
        tensor = img_resized.reshape(1, self.inputHeight, self.inputWidth, self.channels)
        tensor = np.float32(tensor)
        self.interpreter.set_tensor(self.input_details[0]['index'], tensor)
        self.interpreter.invoke()
        ouput_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        embeddings = Facenet.normalize(ouput_data)
        return embeddings

    @staticmethod
    def normalize(embeddings):
        return embeddings / max(np.linalg.norm(embeddings), 1e-12)
