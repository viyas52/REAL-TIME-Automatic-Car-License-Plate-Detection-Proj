# Automatic Car License Plate Detection

## How to run:
### steps :

--> Clone the repository

```bash
https://github.com/viyas52/license-plate-detection-demo1.git
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
python app.py
```