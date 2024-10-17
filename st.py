import streamlit as st
import tempfile
import os
from ALPD.pipeline.training_pipeline import run_pipeline


st.title("Automatic Car License Plate Detection")


uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi"])

if uploaded_file is not None:

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())


    st.video(uploaded_file)

    
    if st.button("Process Video"):
        with st.spinner('Running license plate detection pipeline...'):
            run_pipeline(tfile.name)

        st.success("Video processed successfully!")

        output_dir = os.path.join(os.getcwd(), 'output') 
        output_video_path = os.path.join(output_dir, 'out.mp4')  

       
        if os.path.exists(output_video_path):

            with open(output_video_path, "rb") as file:
                btn = st.download_button(
                    label="Download Processed Video",
                    data=file,
                    file_name="processed_video.mp4",
                    mime="video/mp4"
                )
        else:
            st.error("Processed video not found. Please check the pipeline.")
