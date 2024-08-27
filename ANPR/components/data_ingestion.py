import cv2

def read_video(input_video_path):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise Exception(f"Error: Could not open video '{input_video_path}'")
    return cap
