import csv
import numpy as np
from scipy.interpolate import interp1d


def interpolate_bounding_boxes(data): 
    # Extract necessary data columns from input data
    frame_numbers = np.array([int(row['frame_nmr']) for row in data])
    #print(f'frame number array is {frame_numbers}')
    car_ids = np.array([int(row['car_id']) for row in data])     # you removed a float here 
    #print(f'car ids array is {car_ids}')
    car_bboxes = np.array([list(map(float, row['car_bbox'][1:-1].split())) for row in data])
    #print(f'car boxes array is {car_bboxes}')
    license_plate_bboxes = np.array([list(map(float, row['license_plate_bbox'][1:-1].split())) for row in data])
    #print(f'license plate box array is {license_plate_bboxes}')

    interpolated_data = []
    unique_car_ids = np.unique(car_ids)
    #print(f'unique car ids are {unique_car_ids}')
    for car_id in unique_car_ids:

        frame_numbers_ = [p['frame_nmr'] for p in data if int(float(p['car_id'])) == int(float(car_id))]
        print(frame_numbers_, car_id)
        
        # Filter data for a specific car ID
        car_mask = car_ids == car_id
        #print(f'car mask = {car_mask}')   # bool value --> with its respective car id in all frames is true
        car_frame_numbers = frame_numbers[car_mask]    # same but here it is in int
        #print(f'car frame numbers is {car_frame_numbers}') # in an array for a car id with all the frame number it is present in 
        car_bboxes_interpolated = []
        license_plate_bboxes_interpolated = []

        first_frame_number = car_frame_numbers[0]
        last_frame_number = car_frame_numbers[-1]
        for i in range(len(car_bboxes[car_mask])):
            frame_number = car_frame_numbers[i]
            #print(f'frame number is {frame_number}')
            car_bbox = car_bboxes[car_mask][i]
            #print(f'car box is {car_bbox}')
            license_plate_bbox = license_plate_bboxes[car_mask][i]
            #print(f'license box is {license_plate_bbox}')

            if i > 0:
                prev_frame_number = car_frame_numbers[i-1]
                #print(f'preb frame number is {prev_frame_number}')
                prev_car_bbox = car_bboxes_interpolated[-1]
                #print(f'prev car b is {prev_car_bbox}')
                prev_license_plate_bbox = license_plate_bboxes_interpolated[-1]
                #print(f'prev license b is {prev_license_plate_bbox}')

                if frame_number - prev_frame_number > 1:
                    # Interpolate missing frames' bounding boxes
                    frames_gap = frame_number - prev_frame_number
                    x = np.array([prev_frame_number, frame_number])
                    #print(x)
                    x_new = np.linspace(prev_frame_number, frame_number, num=frames_gap, endpoint=False)
                    #print(x_new)
                    interp_func = interp1d(x, np.vstack((prev_car_bbox, car_bbox)), axis=0, kind='linear')
                    interpolated_car_bboxes = interp_func(x_new)
                    interp_func = interp1d(x, np.vstack((prev_license_plate_bbox, license_plate_bbox)), axis=0, kind='linear')
                    interpolated_license_plate_bboxes = interp_func(x_new)

                    car_bboxes_interpolated.extend(interpolated_car_bboxes[1:])
                    license_plate_bboxes_interpolated.extend(interpolated_license_plate_bboxes[1:])

            car_bboxes_interpolated.append(car_bbox) # both these lines for the 0 th index or the first value 
            license_plate_bboxes_interpolated.append(license_plate_bbox)

        for i in range(len(car_bboxes_interpolated)):
            frame_number = first_frame_number + i
            row = {}
            row['frame_nmr'] = str(frame_number)
            row['car_id'] = str(car_id)
            row['car_bbox'] = ' '.join(map(str, car_bboxes_interpolated[i]))
            row['license_plate_bbox'] = ' '.join(map(str, license_plate_bboxes_interpolated[i]))

            if str(frame_number) not in frame_numbers_:
                # Imputed row, set the following fields to '0'
                row['license_plate_bbox_score'] = '0'
                row['license_number'] = '0'
                row['license_number_score'] = '0'
            else:
                # Original row, retrieve values from the input data if available
                original_row = [p for p in data if int(p['frame_nmr']) == frame_number and int(float(p['car_id'])) == int(float(car_id))][0]
                row['license_plate_bbox_score'] = original_row['license_plate_bbox_score'] if 'license_plate_bbox_score' in original_row else '0'
                row['license_number'] = original_row['license_number'] if 'license_number' in original_row else '0'
                row['license_number_score'] = original_row['license_number_score'] if 'license_number_score' in original_row else '0'

            interpolated_data.append(row)

    return interpolated_data 