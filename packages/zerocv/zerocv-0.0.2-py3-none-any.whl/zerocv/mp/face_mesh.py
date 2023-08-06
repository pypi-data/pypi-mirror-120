import cv2
import mediapipe as mp


# mp_drawing = mp.solutions.drawing_utils
# mp_face_mesh = mp.solutions.face_mesh
# drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

__all__ = ['FaceMesh']

class FaceMesh:
    def __init__(self):
        self.__mp_face_mesh = mp.solutions.face_mesh
        self.__face_mesh = self.__mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.__mp_drawing = mp.solutions.drawing_utils

    def process(self, frame):
        image = frame.copy()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.__face_mesh.process(image) 
        
        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_face_landmarks:
            ret = results.multi_face_landmarks
            for face_landmarks in results.multi_face_landmarks:
                self.__mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.__mp_face_mesh.FACEMESH_TESSELATION, 
                    landmark_drawing_spec = None, 
                    connection_drawing_spec = self.__mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=1, circle_radius=1))
        else:
            ret = []
            
        return image, ret

    def __del__(self):
        if self.__face_mesh:
            self.__face_mesh.close()
