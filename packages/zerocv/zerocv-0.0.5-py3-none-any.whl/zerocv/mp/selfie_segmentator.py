import cv2
import numpy as np
import mediapipe as mp


__all__ = ['SelfieSegmentator']

BG_COLOR = (192, 192, 192) # gray

class SelfieSegmentator:
    def __init__(self):
        self.__mp_drawing = mp.solutions.drawing_utils
        self.__mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.__selfie_segmentation = self.__mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
        self.__bg_image = None

    def process(self, frame):
        image = frame.copy()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.__selfie_segmentation.process(image)
        
       
        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        
        ret = []
        
        if self.__bg_image is None:
            self.__bg_image = np.zeros(image.shape, dtype=np.uint8)
            self.__bg_image[:] = BG_COLOR
        
        output_image  = np.where(condition, image, self.__bg_image)
            
            
        return output_image, ret
    
    def __del__(self):
        if self.__selfie_segmentation:
            self.__selfie_segmentation.close()
