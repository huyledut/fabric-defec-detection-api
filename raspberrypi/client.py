import serial
import cv2
import time
import requests
import pprint
import warnings
from speech import ts
import base64
from io import BytesIO
from PIL import Image
from tool import Read
warnings.filterwarnings("ignore")

ser = serial.Serial("/dev/ttyUSB0", 9600)
ser.reset_input_buffer()
BASE_ORIGIN = 'http://34.126.134.54:8000'
# BASE_ORIGIN = 'https://c82d-2402-800-6294-3859-4896-a912-7627-a253.ngrok-free.app'
DETECTION_URL = f'{BASE_ORIGIN}/api/v1/instance-segmentation/client'
# Khởi tạo camera
camera = cv2.VideoCapture(0)
# Thiết lập kích thước khung hình của camera
camera.set(3, 640) # set chiều rộng khung hình
camera.set(4, 640) # set chiều cao khung hình
ts.Read(message = "Chào mừng bạn đến với hệ thống nhận diện lỗi dệt may!")

state = None
while state != 'Start':
    state = input("Nhap 'Start' de bat dau!\n")

defects = ['Hole', 'Knot', 'Line', 'Stain']
ser.write(state.encode())

while True:
    if  ser.inWaiting()>0: 
        data = ser.readline().decode().strip()
        if data == "Started":
            break 
        # print(data)
    print("123")
    time.sleep(1)

try:
    ser.reset_input_buffer()
    while True:
        if  ser.inWaiting()>0: 
            data = ser.readline()
        else:
            continue
        data = data.decode("utf-8").strip()
        # print(data)
        if data == "A":
            ser.flushInput()
            # take a sample photo
            print("step 1")
            ret, frame = camera.read()
            IMAGE_URL = "detect.jpg"
            cv2.imwrite(IMAGE_URL, frame)
            with open(IMAGE_URL, 'rb') as f:
                image_data = f.read()
            image = cv2.imread(IMAGE_URL)

            # call api to detect
            print("step 2")
            res_detect = set()
            try:
                response = requests.post(DETECTION_URL, files={'file': image_data})
                # result detection
                if response.status_code == 200:
                    data = response.json()
                    detections = data["detections"]
                    base64_image = data["image"]
                    image_data = base64.b64decode(base64_image)
                    image = Image.open(BytesIO(image_data))
                    save_path = "images/response.jpg"
                    image.save(save_path)
                    pprint.pprint(detections)
                    for result in detections:
                        res_detect.add(defects[int(result['class_id'])])
            except Exception as e:
                print(str(e))
                send_data = "B"
                ser.write(send_data.encode())
                time.sleep(2)
                continue
            # read result
            text = "Kết quả kiểm tra:"
            error = []
            if len(res_detect):
                text += "Xuất hiện lỗi "
                for item in res_detect:
                    text += f'{item}, '
                    error.append(item)
            else:
                text += "Vải không xuất hiện lỗi!"
            print(error)
            print("step 3")
            # ts.Read(text)
            Read(error)
            time.sleep(1)
            print("step 4")
            # send data arduino
            send_data = "B"
            ser.write(send_data.encode())

            time.sleep(2)
except KeyboardInterrupt:
    ser.close()