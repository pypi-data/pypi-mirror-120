import cv2

def draw_progress(image, value):
    value = 0.1
    h, w, c = image.shape
    a_h = int(h * 0.8)
    a_w = 30
    
    p_h = int(a_h * value)
    image = cv2.rectangle(image, (10, 10), (10+a_w, 10+a_h), (0, 255, 0), 5, cv2.LINE_8)
    image = cv2.rectangle(image, (10, 10+a_h-p_h), (10+a_w, 10+a_h), (0, 255, 0), -1)
    return image
