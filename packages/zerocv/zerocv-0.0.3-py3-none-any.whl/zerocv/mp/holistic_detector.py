import cv2
import mediapipe as mp

__all__ = ['HolisticDetector']

class HolisticDetector:
    def __init__(self):
        self.__mp_drawing = mp.solutions.drawing_utils
        self.__mp_holistic = mp.solutions.holistic
        self.__holistic = self.__mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def process(self, frame):
        image = frame.copy()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.__holistic.process(image) 
        
        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.face_landmarks:
            face = results.face_landmarks
            self.__mp_drawing.draw_landmarks(
                image, 
                results.face_landmarks, 
                self.__mp_holistic.FACEMESH_TESSELATION,
                None,
                self.__mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=1, circle_radius=1))
        else:
            face = []
            

        if results.pose_landmarks:
            pose = results.pose_landmarks
            self.__mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                self.__mp_holistic.POSE_CONNECTIONS,
                self.__mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4), 
                self.__mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))
        else:
            pose = []
            
        return image, (face, pose)

    def __del__(self):
        if self.__holistic:
            self.__holistic.close()
