from fastapi import FastAPI, File
from util.services import get_yolov5, get_image_from_bytes
from starlette.responses import Response
from io import BytesIO
from PIL import Image
import json
from fastapi.middleware.cors import CORSMiddleware


model = get_yolov5()

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


@app.get('api/v1/health')
def get_health():
    return dict(msg='OK')


@app.post("api/v1/object-to-json")
async def detect_return_json_result(file: bytes = File(...)):
    input_image = get_image_from_bytes(file, max_size=640)
    results = model(input_image, size=640)
    detect_res = results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions
    detect_res = json.loads(detect_res)
    return {"result": detect_res}


@app.post("api/v1/object-to-img")
async def detect_return_base64_img(file: bytes = File(...)):
    input_image = get_image_from_bytes(file, max_size=640)
    results = model(input_image)
    results.ims # array of original images (as np array) passed to model for inference
    results.render()  # updates results.ims with boxes and labels
    for im in results.ims:
        buffered = BytesIO()
        im_base64 = Image.fromarray(im)
        im_base64.save(buffered, format="JPEG")
    return Response(content=buffered.getvalue(), media_type="image/jpeg")