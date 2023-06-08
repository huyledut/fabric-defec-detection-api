import torch
from PIL import Image
import io
from helper.segment.predict import run
from pathlib import Path
from helper.models.common import DetectMultiBackend

def load_yolov5_obj():
    torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = torch.hub.load('helper',model= 'custom', path='./models/obj-v2', source= 'local')
    model.conf = 0.20
    return model

def load_model_seg():
    weights = 'models/seg-v1.pt'
    data = 'util/dataset.yaml'
    return DetectMultiBackend(weights=weights, data=data)

def seg_run(model, name='result', weights = './models/seg-v1.pt', source = 'image.jpg', project= Path.cwd()):
    run(weights=weights, source=source, data='', name=name, project=project, save_txt=True, save_conf=True, exist_ok=True, model=model)

def get_image_from_bytes(binary_image, max_size=1024):
    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    width, height = input_image.size
    resize_factor = min(max_size / width, max_size / height)
    resized_image = input_image.resize(
        (
            int(input_image.width * resize_factor),
            int(input_image.height * resize_factor),
        )
    )
    return resized_image

def save_uploaded_image(image_bytes):
    file_path = "images/request.jpg"
    with open(file_path, "wb") as f:
        f.write(image_bytes)
