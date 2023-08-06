import cv2
import mediapipe as mp

__all__ = ['FaceDetector']

class FaceDetector:
    def __init__(self):
        self.__mp_face_detection = mp.solutions.face_detection
        self.__mp_drawing = mp.solutions.drawing_utils
        # drawing_spec = self.__mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4)
        self.__face_detection = self.__mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

    
    def process(self, frame):
        frame = frame.copy()
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = self.__face_detection.process(frame) 
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if results.detections:
            ret = results.detections
            for detection in results.detections:
                self.__mp_drawing.draw_detection(frame, detection, 
                                                 self.__mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4), 
                                                 self.__mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))
        else:
            ret = []
            
        return frame, ret

    def __del__(self):
        '''
        del facedetector
        '''
        if self.__face_detection:
            self.__face_detection.close()
