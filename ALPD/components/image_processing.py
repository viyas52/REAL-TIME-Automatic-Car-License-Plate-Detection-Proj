import cv2
import numpy as np

def preprocess_image(image):
    denoised = cv2.fastNlMeansDenoising(image, None, 3, 5, 15)
    blurred = cv2.GaussianBlur(denoised, (5, 5), 0)
    sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(blurred, -1, kernel=sharpening_kernel)
    return sharpened
