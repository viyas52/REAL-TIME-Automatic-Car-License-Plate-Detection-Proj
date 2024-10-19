# Automatic Car License Plate Detection

This project is an end-to-end solution for automatic car license plate detection, recognition, and vehicle tracking. It uses deep learning models(YOLOv10) for accurate detection, OCR for plate recognition, and integrates a MySQL database for storing and verifying authorized license plates.

## How to run:
### steps :

--> Clone the repository

```bash
https://github.com/viyas52/Automatic-Car-License-Plate-Detection-Proj.git
```

--> Also clone the open source "sort" repository for multiple object tracking 

```bash
https://github.com/viyas52/sort.git
```


--> Create a conda environment and activate it

```bash
conda create -n ALPR python=3.9 -y
```

```bash
conda activate ALPR
```

--> Install the requirements

```bash
pip install -r requirements.txt
```

--> Also install the cuda and pytorch libraries according to your system configuration
-- run this to check it

```bash
python testing.py
```

--> To run the application, type this in the terminal

```bash
python st.py
```

#for ec2
#optinal
```bash
sudo apt-get update -y
```

```bash
sudo apt-get upgrade
```

#required
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
```
```bash
sudo sh get-docker.sh
```
```bash
sudo usermod -aG docker ubuntu
```
```bash
newgrp docker
```