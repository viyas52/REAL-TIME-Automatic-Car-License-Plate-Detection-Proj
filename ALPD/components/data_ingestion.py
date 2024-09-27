import cv2

def read_video(input_video_path):
    cap = cv2.VideoCapture(input_video_path)
    return cap
