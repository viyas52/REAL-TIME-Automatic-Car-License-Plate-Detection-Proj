from ultralytics import YOLO
import cv2
import os
from sort.sort import *
from utils import *
import matplotlib.pyplot as plt
import numpy as np

results={}
mot_tracker = Sort()

coco_model = YOLO("models/yolov10n.pt")

license_plate_detector = YOLO("models/BLPDM.pt")


input_video_path = 'demos/demo2.mp4'
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)


cap = cv2.VideoCapture(input_video_path)

if not cap.isOpened():
    print(f"Error: Could not open video '{input_video_path}'")
    exit()
    
frame_nmr=-1
vehicals = [2,5,7]
ret = True
while ret :
    frame_nmr+=1
    ret,frame = cap.read()
    
    if ret :
        results[frame_nmr] = {}
        detections = coco_model(frame)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicals:
                detections_.append([x1, y1, x2, y2, score])
                
        trac_ids = mot_tracker.update(np.asarray(detections_))
        
        
        license_plates = license_plate_detector(frame)[0]
        license_ = []
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, trac_ids)
            
            if car_id != -1:
                license_plate_crop = frame[int(y1):int(y2),int(x1):int(x2)]
            
                denoised = cv2.fastNlMeansDenoising(license_plate_crop, None, 3, 5, 15)
                
                blurred = cv2.GaussianBlur(denoised, (5, 5), 0)
                
                sharpening_kernel = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]]) 
                
                sharpened = cv2.filter2D(blurred, -1, kernel=sharpening_kernel)
                
                # cv2.imshow('license croped',license_plate_crop)
                # cv2.imshow('license denoised',denoised)
                # cv2.imshow('license blurred',blurred)
                # cv2.imshow('license sharpened',sharpened)
                # cv2.imshow('license threshold',license_plate_crop_thresh)
                # cv2.waitKey(0)
                
                preprocessed_image_for_ocr = convert_to_np_array(sharpened)
                
                license_plate_text, license_plate_text_score = read_license_plate(preprocessed_image_for_ocr)
                
                if license_plate_text is not None:
                    results[frame_nmr][int(car_id)] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                    'text': license_plate_text,
                                                                    'bbox_score': score,
                                                                    'text_score': license_plate_text_score}}
            
        
        


write_csv(results,'./test.csv')
