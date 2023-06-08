import base64
from io import BytesIO
import pprint
import cv2
import requests
from PIL import Image


DETECTION_URL = 'http://127.0.0.1:8000/api/v1/instance_segmentation/client'
IMAGE = 'images/image.jpg'

image = cv2.imread(IMAGE)
resized_image = cv2.resize(image, (640, 640))
is_success, img_bytes = cv2.imencode('.jpg', resized_image)

if is_success is not True:
    print("ERROR")

response = requests.post(DETECTION_URL, files={'file': img_bytes})
if response.status_code == 200:
    data = response.json()
    detections = data["detections"]
    base64_image = data["image"]
    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data))
    pprint.pprint(detections)
    save_path = "images/response.jpg"
    image.save(save_path)
    image.show()

