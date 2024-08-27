from ANPR.constants.password import *

'''
Constants for ANPR Project
'''

coco_model_path:str = "models/yolov10n.pt"

license_plate_model_path:str = "models/BLPDM.pt"

input_video_path:str = "demos/demo.mp4"

output_dir:str = "output"

raw_csv:str = 'res/test.csv'

interpolated_csv:str = 'res/test_interpolated.csv'

output_video:str = 'output/out.mp4'

mysql_password:str = sql

database_name:str = 'license_plate_db'
