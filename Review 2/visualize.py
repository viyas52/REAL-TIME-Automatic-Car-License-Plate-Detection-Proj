import ast
import cv2
import numpy as np
import pandas as pd

def draw_border(img, top_left, bottom_right, color=(0, 0, 255), thickness=5, line_length_x=150, line_length_y=150):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.line(img, (x1, y1), (x1, y1 + line_length_y), color, thickness)  #-- top-left
    cv2.line(img, (x1, y1), (x1 + line_length_x, y1), color, thickness)

    cv2.line(img, (x1, y2), (x1, y2 - line_length_y), color, thickness)  #-- bottom-left
    cv2.line(img, (x1, y2), (x1 + line_length_x, y2), color, thickness)

    cv2.line(img, (x2, y1), (x2 - line_length_x, y1), color, thickness)  #-- top-right
    cv2.line(img, (x2, y1), (x2, y1 + line_length_y), color, thickness)

    cv2.line(img, (x2, y2), (x2, y2 - line_length_y), color, thickness)  #-- bottom-right
    cv2.line(img, (x2, y2), (x2 - line_length_x, y2), color, thickness)

    return img

results = pd.read_csv('./test_interpolated.csv', encoding='ISO-8859-1')

# Load video
video_path = 'demos/demo2.mp4'
cap = cv2.VideoCapture(video_path)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output/out22.mp4', fourcc, fps, (width, height))

license_plate = {}
for car_id in np.unique(results['car_id']):
    max_ = np.amax(results[results['car_id'] == car_id]['license_number_score'])
    license_plate[car_id] = {'license_crop': None,
                             'license_plate_number': results[(results['car_id'] == car_id) &
                                                             (results['license_number_score'] == max_)]['license_number'].iloc[0]}
    cap.set(cv2.CAP_PROP_POS_FRAMES, results[(results['car_id'] == car_id) &
                                             (results['license_number_score'] == max_)]['frame_nmr'].iloc[0])
    ret, frame = cap.read()

frame_nmr = -1

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

# Read frames
ret = True
while ret:
    ret, frame = cap.read()
    frame_nmr += 1
    if ret:
        df_ = results[results['frame_nmr'] == frame_nmr]
        for row_indx in range(len(df_)):
            # Draw car
            car_x1, car_y1, car_x2, car_y2 = ast.literal_eval(df_.iloc[row_indx]['car_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
            draw_border(frame, (int(car_x1), int(car_y1)), (int(car_x2), int(car_y2)), (255, 0, 0), 10,
                        line_length_x=100, line_length_y=100)

            # Draw license plate bounding box
            x1, y1, x2, y2 = ast.literal_eval(df_.iloc[row_indx]['license_plate_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 7)

            # Get license plate text
            license_plate_text = license_plate[df_.iloc[row_indx]['car_id']]['license_plate_number']

            # Define text background
            text_bg_color = (255, 255, 255)  # White background
            text_color = (0, 0, 0)  # Black text

            # Define text size and position
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 3
            thickness = 6
            (text_width, text_height), _ = cv2.getTextSize(license_plate_text, font, font_scale, thickness)

            # Update text_x and text_y to place the text above the license plate bounding box
            text_x = int((x1 + x2 - text_width) / 2)
            text_y = int(y1 - text_height - 20)

            # Draw white rectangle as background for text
            cv2.rectangle(frame, (text_x - 10, text_y - text_height - 10), (text_x + text_width + 10, text_y + 10), text_bg_color, cv2.FILLED)

            # Put text on the frame
            cv2.putText(frame, license_plate_text, (text_x, text_y), font, font_scale, text_color, thickness)

        out.write(frame)
        frame = cv2.resize(frame, (1280, 720))

        # cv2.imshow('frame', frame)
        # cv2.waitKey(0)

out.release()
cap.release()

