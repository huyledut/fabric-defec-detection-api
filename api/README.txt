### FABRIC DEFECT DETECTION API 

## install virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## run api
uvicorn main:app --reload

## The error message indicates that the library "libGL.so.1" cannot be found
sudo apt-get update
sudo apt-get install libgl1-mesa-glx