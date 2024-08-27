def validate_video(cap):
    if not cap.isOpened():
        raise ValueError("Invalid video stream.")
