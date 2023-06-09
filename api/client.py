import base64
from io import BytesIO
import pprint
import cv2
import requests
from PIL import Image


DETECTION_URL = 'https://c82d-2402-800-6294-3859-4896-a912-7627-a253.ngrok-free.appapi/v1/instance-segmentation/client'
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

