from ultralytics import YOLO
import cv2
import os
from sort.sort import *
from utils import *
import numpy as np

results = {}
mot_tracker = Sort()

coco_model = YOLO("models/yolov10n.pt")
license_plate_detector = YOLO("models/BLPDM.pt")

output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# Open video capture for the default camera (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

frame_nmr = -1
vehicals = [2, 5, 7]
ret = True

while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    
    if ret:
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
                license_plate_crop = frame[int(y1):int(y2), int(x1):int(x2)]
                
                denoised = cv2.fastNlMeansDenoising(license_plate_crop, None, 3, 5, 15)
                blurred = cv2.GaussianBlur(denoised, (5, 5), 0)
                sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                sharpened = cv2.filter2D(blurred, -1, kernel=sharpening_kernel)
                
                preprocessed_image_for_ocr = convert_to_np_array(sharpened)
                license_plate_text, license_plate_text_score = read_license_plate(preprocessed_image_for_ocr)
                
                if license_plate_text is not None:
                    results[frame_nmr][int(car_id)] = {
                        'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                        'license_plate': {
                            'bbox': [x1, y1, x2, y2],
                            'text': license_plate_text,
                            'bbox_score': score,
                            'text_score': license_plate_text_score
                        }
                    }
        
        # Optionally, display the frame with detections
        # (You may want to draw bounding boxes and text on the frame)
        cv2.imshow('Live License Plate Detection', frame)
        
        # Write results to CSV file periodically or based on some condition
        write_csv(results, './test.csv')

        # Exit loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
