import numpy as np
import cv2
import os

__all__ = ['FaceDetector']

class FaceDetector:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        # self.__facenet = cv2.dnn.readNet(os.path.join(cur_dir, 'models', 'deploy.prototxt'), 
        #                                 os.path.join(cur_dir, 'models', 'res10_300x300_ssd_iter_140000.caffemodel'))

    def load_model(self, prototxt, model):
        """
        deploy.prototxt
        res10_300x300_ssd_iter_140000.caffemodel
        """
        self.__facenet = cv2.dnn.readNet(prototxt, model)
        
    def process(self, frame):
        frame = frame.copy()
        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, scalefactor=1., size=(300, 300), mean=(104., 177., 123.))
        self.__facenet.setInput(blob)
        dets = self.__facenet.forward()
        
        ret = []
        for i in range(dets.shape[2]):
            confidence = dets[0, 0, i, 2]
            if confidence < 0.8:
                continue

            x1 = int(dets[0, 0, i, 3] * w)
            y1 = int(dets[0, 0, i, 4] * h)
            x2 = int(dets[0, 0, i, 5] * w)
            y2 = int(dets[0, 0, i, 6] * h)
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness=2, lineType=1)
            
            ret.append([i, x1, y1, x2, y2])
        return frame, ret

    def __del__(self):
        '''
        del facedetector
        '''
        pass