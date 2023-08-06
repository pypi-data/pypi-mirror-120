import os
import cv2
import numpy as np


__all__ = ['ObjectDetector']

whT = 320
confThreshold = 0.5
nmsThreshold = 0.2

class ObjectDetector:
    def __init__(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.__net = cv2.dnn.readNet(os.path.join(cur_dir, 'yolov3.cfg'), os.path.join(cur_dir, 'yolov3.weights'))
        # self.__net = cv2.dnn.readNetFromDarknet("C:\\_prj_\\zerocv\\zerocv\\zerocv\\yolo3\\yolov3.cfg", 
        #                                         os.path.join(cur_dir, "yolov3.weights"))
        self.__net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.__net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        
        self.__target = []
        self.__classNames = []
        self.__read_namesfile()
    
    def __read_namesfile(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(cur_dir, 'coco.names'), 'rt') as f:
            self.__classNames = f.read().rstrip('\n').split('\n')

    def __findObjects(self, outputs, image):
        hT, wT, cT = image.shape
        bbox = []
        classIds = []
        confs = []

        ret = []
        label = []
        
        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThreshold:
                    w,h = int(det[2]*wT) , int(det[3]*hT)
                    x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
                    bbox.append([x,y,w,h])
                    classIds.append(classId)
                    confs.append(float(confidence))

        indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

        for i in indices:
            i = i[0]
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            
            if len(self.__target) == 0:
                # print(x,y,w,h)
                cv2.rectangle(image, (x, y), (x+w,y+h), (250, 44, 250), 2)
                cv2.putText(image, f'{self.__classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            
                ret.append([x, y, x+w, y+h])
                label.append(self.__classNames[classIds[i]].lower())
            else:
                if self.__classNames[classIds[i]].lower() in self.__target:
                    cv2.rectangle(image, (x, y), (x+w,y+h), (250, 44, 250), 2)
                    cv2.putText(image, f'{self.__classNames[classIds[i]].upper()} {int(confs[i]*100)}%', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
                
                    ret.append([x, y, x+w, y+h])
                    label.append(self.__classNames[classIds[i]].lower())
                    

        return image, (ret, label)


    def process(self, frame):
        image = frame.copy()
        blob = cv2.dnn.blobFromImage(image, 1 / 255, (320, 320), [0, 0, 0], 1, crop=False)
        self.__net.setInput(blob)
        
        layersNames = self.__net.getLayerNames()
        outputNames = [(layersNames[i[0] - 1]) for i in self.__net.getUnconnectedOutLayers()]
        outputs = self.__net.forward(outputNames)
        return self.__findObjects(outputs, image)

    def classes(self):
        return self.__classNames

    def set_labels(self, labels):
        self.__target = labels


    def __del__(self):
        pass
