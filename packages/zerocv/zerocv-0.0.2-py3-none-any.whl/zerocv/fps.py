import time
import cv2

__all__ = ['FPS']

class FPS:

    def __init__(self):
        self.__time = time.time()

    def update(self, frame=None, pos=(20, 50), color=(0, 255, 0), scale=3, thickness=3):
        cur_time = time.time()
        try:
            fps = 1 / (cur_time - self.__time)
            self.__time = cur_time
            if frame is None:
                return fps
            else:
                cv2.putText(frame, f'FPS: {int(fps)}', pos, cv2.FONT_HERSHEY_PLAIN, scale, color, thickness)
                return fps, frame
        except:
            return 0
