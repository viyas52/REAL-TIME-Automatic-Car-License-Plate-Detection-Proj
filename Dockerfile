FROM python:3.8-slim-buster

# Install required libraries
RUN apt-get update && \
    apt-get install -y libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "st.py"]
