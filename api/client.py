import pprint
import cv2
import requests
from PIL import Image

DETECTION_URL = 'http://127.0.0.1:8000/api/v1/object-to-json'
IMAGE = 'image.jpg'

# đọc hình ảnh
image = cv2.imread(IMAGE)
resized_image = cv2.resize(image, (640, 640))
is_success, img_bytes = cv2.imencode('.jpg', resized_image)

# Read imageabc
# with open(IMAGE, 'rb') as f:
#     image_data = f.read()
if is_success is not True:
    print("ERROR")

response = requests.post(DETECTION_URL, files={'file': img_bytes}).json()

for result in response:
    xmin = int(result['xmin'])
    ymin = int(result['ymin'])
    xmax = int(result['xmax'])
    ymax = int(result['ymax'])
    label = str(round(result['confidence'] * 100)) + '% ' + result['name']
    color = (0, 255, 0) # màu xanh lá cây
    thickness = 2
    cv2.rectangle(resized_image, (xmin, ymin), (xmax, ymax), color, thickness)

    # css
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5 # tỷ lệ kích thước của chữ
    text_color = (0, 255, 0) # màu xanh lá cây
    text_thickness = 2 # độ dày của chữ
    text_size, _ = cv2.getTextSize(label, font, font_scale, text_thickness)

    cv2.putText(resized_image, label, (xmin, ymin - text_size[1]), font, font_scale, text_color, text_thickness)

pprint.pprint(response)

URL_RESPONSE = "response.jpg"
cv2.imwrite(URL_RESPONSE, resized_image)
res = cv2.imread(URL_RESPONSE)
cv2.imshow("response", res)
cv2.waitKey(2)
