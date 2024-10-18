FROM python:3.8-slim-buster

# Install required libraries
RUN apt-get update && apt-get install -y libgl1-mesa-glx

    
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "st.py"]
