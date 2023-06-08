import base64
from fastapi import FastAPI, File
from util.services import load_yolov5_obj, get_image_from_bytes, load_model_seg, seg_run, save_uploaded_image
from starlette.responses import Response
from io import BytesIO
from PIL import Image
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

obj_model = load_yolov5_obj()
seg_model = load_model_seg()

app = FastAPI(
    title="DUT-CAPSTONE-PROJECT",
    description="""Obtain object value out of image
                    and return image and json result""",
    version="0.0.1",
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/v1/health')
def get_health():
    return dict(msg='OK')


@app.post("/api/v1/object-detection/to-json")
async def object_detection_return_json(file: bytes = File(...)):
    input_image = get_image_from_bytes(file, max_size=640)
    results = obj_model(input_image, size=640)
    print(results.xyxy)
    detect_res = results.pandas().xyxy[0].to_json(orient="records")
    detect_res = json.loads(detect_res)
    return detect_res


@app.post("/api/v1/object-detection/to-img")
async def object_detection_return_image(file: bytes = File(...)):
    input_image = get_image_from_bytes(file, max_size=640)
    results = obj_model(input_image)
    results.ims
    results.render()
    for im in results.ims:
        buffered = BytesIO()
        im_base64 = Image.fromarray(im)
        im_base64.save(buffered, format="JPEG")
    return Response(content=buffered.getvalue(), media_type="image/jpeg")


@app.post("/api/v1/object-detection/client")
async def object_detection_return_for_client(file: bytes = File(...)):
    input_image = get_image_from_bytes(file, max_size=640)
    results = obj_model(input_image)
    results.render()
    detect_res = results.pandas().xyxy[0].to_json(orient="records")
    detect_res = json.loads(detect_res)
    buffered = BytesIO()
    im_base64 = Image.fromarray(results.ims[0])
    im_base64.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    response = {
        "detections": detect_res,
        "image": base64_image
    }
    return response

@app.post("/api/v1/instance-segmentation/to-img")
async def instance_segmentation_return_image(file: bytes = File(...)):
    input_image = get_image_from_bytes(file, max_size=640)
    save_uploaded_image(file)
    seg_run(source="images/request.jpg", model=seg_model)
    result = 'output_image.jpg'
    return FileResponse(result, media_type="image/jpeg")

@app.post("/api/v1/instance-segmentation/client")
async def instance_segmentation_return_for_client(file: bytes = File(...)):
    input_image = get_image_from_bytes(file, max_size=640)
    save_uploaded_image(file)
    seg_run(source="images/request.jpg", model=seg_model)

    with open('result/labels/request.txt', 'r') as lbl_file:
        label_data = lbl_file.readlines()
        detections = []
        for line in label_data:
            data= line.strip().split()
            object_info = {
                "class_id": data[0],
                "conf": data[-1]
            }
            detections.append(object_info)
        lbl_file.close()
    with open('output_image.jpg', 'rb') as img_file:
        image_data = img_file.read()

    response = {
        "detections": detections,
        "image": base64.b64encode(image_data).decode("utf-8")
    }
    return response