from ANPR.pipeline.training_pipeline import run_pipeline
coco_model_path = "models/yolov10n.pt"
license_plate_model_path = "models/BLPDM.pt"
input_video_path = 'demos/demo9.mp4'
output_dir = 'output'


obj = run_pipeline(coco_model_path,license_plate_model_path,input_video_path,output_dir)
