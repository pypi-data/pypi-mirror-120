import os
import cv2
import numpy as np

__all__ = ['Video', 'VideoWriter']

class Video:
    def __init__(self, file_path):
        self.__name = file_path
        self.__capture = cv2.VideoCapture(file_path)
        self.__width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__frame_count = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT)) # 총프레임수
        self.__frame_rate = int(self.__capture.get(cv2.CAP_PROP_FPS)) # 프레임레이트(fps)
        self.__fps = self.__frame_rate


    def read(self):
        if(self.__capture.get(cv2.CAP_PROP_POS_FRAMES) == self.__capture.get(cv2.CAP_PROP_FRAME_COUNT)):
            print('영상 재상이 끝났습니다')
            return np.zeros((self.__height, self.__width))
        
        ret, frame = self.__capture.read()
        if ret:
            return frame
        else:
            return np.zeros((self.__height, self.__width))

    @property
    def is_end(self):
        return (self.__capture.get(cv2.CAP_PROP_POS_FRAMES) == self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))
    
    @property
    def options(self):
        return {
            'height': self.__height,
            'width':self.__width,
            'fps': self.__fps
        }

    @property
    def frame_count(self):
        return self.__frame_count

    def release(self):
        # body of destructor
        if self.__capture is not None:
            self.__capture.release()
            self.__capture = None

    def __del__(self):
        # body of destructor
        if self.__capture is not None:
            self.__capture.release()


class VideoWriter:
    def __init__(self, capture, file_path):
        self.__capture = capture
        self.__width = int(self.__capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.__height = int(self.__capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.__frame_count = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT)) # 총프레임수
        self.__frame_rate = int(self.__capture.get(cv2.CAP_PROP_FPS)) # 프레임레이트(fps)
        self.__fps = self.__frame_rate
        
        self.__fcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.__out = cv2.VideoWriter(file_path, self.__fcc, self.__fps, (self.__width, self.__height))
        self.__writable = False
        self.__frame_count = 0
        # avi
        # self.__fcc = cv2.VideoWriter_fourcc(*'XVID')
        # self.__out = cv2.VideoWriter(os.path.join(path, f'{name}.avi'), self.__fcc, self.__fps, (self.__width, self.__height))
        # print('recorder name :', os.path.join(path, f'{name}.avi'))
        
        # mp4
        # self.__fcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # self.__out = cv2.VideoWriter(os.path.join(path, f'{name}.mp4'), self.__fcc, self.__fps, (self.__width, self.__height))
        # print('recorder name :', os.path.join(path, f'{name}.mp4'))

    @property
    def frame_count(self):
        return self.__frame_count

    def write(self, frame):
        if self.__out:
            self.__frame_count += 1
            self.__out.write(frame)

    def release(self):
        if self.__out is not None:
            self.__out.release()
            self.__out = None

    def __del__(self):
        if self.__out is not None:
            self.__out.release()

