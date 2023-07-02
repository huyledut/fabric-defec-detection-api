import torch
from PIL import Image, ImageDraw, ImageFont
import io
from helper.segment.predict import run
from pathlib import Path
from helper.models.common import DetectMultiBackend
import os

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
    if os.path.exists('result/labels/request.txt'):
        os.remove('result/labels/request.txt')
    run(weights=weights, source=source, data='', name=name, project=project, save_txt=True, save_conf=True, exist_ok=True, model=model, conf_thres=0.25)
    merge_images()

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

def merge_images():
    original_image_path = "images/request.jpg"
    detected_image_path = "result/request.jpg"
    output_image_path = "output_image.jpg"
    original_image = Image.open(original_image_path)
    detected_image = Image.open(detected_image_path)
    merged_width = original_image.width + detected_image.width
    merged_height = max(original_image.height, detected_image.height)
    merged_image = Image.new("RGB", (merged_width, merged_height), color=(255, 255, 255))
    merged_image.paste(original_image, (0, 0))
    merged_image.paste(detected_image, (original_image.width, 0))
    send_label = "Send"
    send_font = ImageFont.truetype("font/Roboto-Black.ttf", size=22)
    send_color = (0, 0, 255)
    send_background = (255, 255, 255)
    send_label_width, send_label_height = send_font.getsize(send_label)
    draw = ImageDraw.Draw(merged_image)
    draw.rectangle([(10, 10), (10 + send_label_width, 10 + send_label_height)], fill=send_background)
    draw.text((10, 10), send_label, font=send_font, fill=send_color)
    result_label = "Result"
    result_font = ImageFont.truetype("font/Roboto-Black.ttf", size=22)
    result_color = (255, 0, 0)
    result_background = (255, 255, 255)
    result_label_width, result_label_height = result_font.getsize(result_label)
    draw.rectangle([(original_image.width + 10, 10),
                    (original_image.width + 10 + result_label_width, 10 + result_label_height)],
                   fill=result_background)
    draw.text((original_image.width + 10, 10), result_label, font=result_font, fill=result_color)
    merged_image.save(output_image_path)
