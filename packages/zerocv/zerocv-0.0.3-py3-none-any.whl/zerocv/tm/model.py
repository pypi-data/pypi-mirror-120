import cv2
import numpy as np
from tensorflow import keras

__all__ = ['ZModel', 'load_model']


class ZModel:
    def __init__(self, model):
        self.__model = model

    def summary(self):
        self.__model.summary()

    def __preprocessing(self, frame):
        #frame_fliped = cv2.flip(frame, 1)
        size = (224, 224)
        frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
        frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
        frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
        return frame_reshaped

    def __center_crop(self, frame):
        height, width = frame.shape[:2]
        crop_len = min(height, width)

        mid_x, mid_y = int(width/2), int(height/2)
        cw2, ch2 = int(crop_len/2), int(crop_len/2) 
        crop_img = frame[mid_y-ch2:mid_y+ch2, mid_x-cw2:mid_x+cw2]
        return crop_img
    
    def predict(self, frame):
        frame = self.__center_crop(frame)
        frame = self.__preprocessing(frame)
        prediction = np.argmax(self.__model.predict(frame))
        return prediction


def load_model(model_path):
    model = keras.models.load_model(model_path)
    return ZModel(model)
