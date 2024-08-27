import os
import csv
import numpy as np
import pandas as pd

import mysql.connector

from sort.sort import Sort  # An open source realtime multiple object tracking program , clone this repository into your project folder

from ANPR.components.data_ingestion import read_video
from ANPR.components.data_validation import validate_video
from ANPR.components.model_runner import load_yolo_model, run_inference
from ANPR.components.visualize import draw_border,process_video
from ANPR.components.db import *
from ANPR.components.image_processing import preprocess_image
from ANPR.components.add_missing_data import interpolate_bounding_boxes
from ANPR.utils import *
from ANPR.constants import *




def run_pipeline():
    coco_model = load_yolo_model(coco_model_path)
    license_plate_detector = load_yolo_model(license_plate_model_path)
    
    cap = read_video(input_video_path)
    validate_video(cap)
    
    os.makedirs(output_dir, exist_ok=True)
    
    mot_tracker = Sort()
    vehicals = [2, 5, 7]
    frame_nmr = -1
    ret = True
    results = {}
    
    while ret:
        frame_nmr += 1
        ret, frame = cap.read()
        
        if ret:
            detections = run_inference(coco_model, frame)
            trac_ids = mot_tracker.update(np.asarray([[x1, y1, x2, y2, score] for x1, y1, x2, y2, score, class_id in detections.boxes.data.tolist() if int(class_id) in vehicals]))
            
            license_plates = run_inference(license_plate_detector, frame)
            
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate
                xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, trac_ids)
                
                if car_id != -1:
                    license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2)]
                    preprocessed_image_for_ocr = preprocess_image(license_plate_crop)
                    license_plate_text, license_plate_text_score = read_license_plate(preprocessed_image_for_ocr)
                    
                    if license_plate_text is not None:
                        if frame_nmr not in results:
                            results[frame_nmr] = {}
                        results[frame_nmr][int(car_id)] = {
                            'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                            'license_plate': {
                                'bbox': [x1, y1, x2, y2],
                                'text': license_plate_text,
                                'bbox_score': score,
                                'text_score': license_plate_text_score
                            }
                        }
    

    
    write_csv(results, raw_csv)
    with open(raw_csv, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    
    interpolated_data = interpolate_bounding_boxes(data)
    
    header = ['frame_nmr', 'car_id', 'car_bbox', 'license_plate_bbox', 'license_plate_bbox_score', 'license_number', 'license_number_score']
    with open(interpolated_csv, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(interpolated_data)
    
    results = pd.read_csv(interpolated_csv, encoding='ISO-8859-1')

   
    cap = cv2.VideoCapture(input_video_path)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    process_video(results,cap,out)

    conn = mysql.connector.connect(host='localhost', user='root', password=mysql_password, database=database_name)
    
    create_table(conn)
    
    results = pd.read_csv(raw_csv, encoding='ISO-8859-1')
    process_results(conn, results)
    
    conn.close()
    
    
    
