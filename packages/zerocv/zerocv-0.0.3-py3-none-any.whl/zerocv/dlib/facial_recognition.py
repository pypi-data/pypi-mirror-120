import dlib
import numpy as np
import cv2
import os

__all__ = ['FacialRecognition']


class FacialRecognition:
    def __init__(self):
        # cur_dir = os.path.dirname(os.path.abspath(__file__))
        # self.__detector = dlib.get_frontal_face_detector()
        # self.__sp = dlib.shape_predictor(os.path.join(cur_dir, 'models', 'shape_predictor_68_face_landmarks.dat'))
        # self.__facerec = dlib.face_recognition_model_v1(os.path.join(cur_dir, 'models', 'dlib_face_recognition_resnet_model_v1.dat'))
        self.__descs = None

    def load_model(self, landmarks, model):
        self.__detector = dlib.get_frontal_face_detector()
        self.__sp = dlib.shape_predictor(landmarks)
        self.__facerec = dlib.face_recognition_model_v1(model)
        self.__descs = None
        
        
        
    def __find_faces(self, img):
        dets = self.__detector(img, 1)

        if len(dets) == 0:
            return np.empty(0), np.empty(0), np.empty(0)
        
        rects, shapes = [], []
        shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)
        for k, d in enumerate(dets):
            rect = ((d.left(), d.top()), (d.right(), d.bottom()))
            rects.append(rect)

            shape = self.__sp(img, d)
            
            # convert dlib shape to numpy array
            for i in range(0, 68):
                shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)

            shapes.append(shape)
            
        return rects, shapes, shapes_np


    def __encode_faces(self, img, shapes):
        face_descriptors = []
        for shape in shapes:
            face_descriptor = self.__facerec.compute_face_descriptor(img, shape)
            face_descriptors.append(np.array(face_descriptor))

        return np.array(face_descriptors)

    def read_db(self, db):
        descs = np.load(db, allow_pickle=True)
        self.__descs = descs.item()
    
    def regist(self, images):
        descs = {}
        for name, img_path in images.items():
            img_bgr = cv2.imread(img_path)
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

            _, img_shapes, _ = self.__find_faces(img_rgb)
            descs[name] = self.__encode_faces(img_rgb, img_shapes)[0]
            self.__descs = descs
        return descs


    def process(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rects, shapes, _ = self.__find_faces(img_rgb)
        descriptors = self.__encode_faces(img_rgb, shapes)

        ret = []
        for i, desc in enumerate(descriptors):
            ret = []
            found = False
            for name, saved_desc in self.__descs.items():
                dist = np.linalg.norm([desc] - saved_desc, axis=1)
                if dist < 0.6:
                    found = True
                    cv2.putText(frame, name, (rects[i][0][0], rects[i][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (rects[i][0][0], rects[i][0][1]), (rects[i][1][0], rects[i][1][1]),(0, 255, 0), 2  )
                ret.append([name, found])

        return frame, ret


    def __del__(self):
        pass