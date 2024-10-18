FROM python:3.8-slim-buster

RUN apt update -y && \
    apt install -y awscli libgl1
    
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "st.py"]
