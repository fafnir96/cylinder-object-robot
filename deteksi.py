import torch
import cv2
import numpy as np
from pathlib import Path
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords
from utils.torch_utils import select_device

# === CONFIGURASI ===
weights_path = 'runs/train/tiny-100epoch/weights/best.pt'  # Ganti dengan path model kamu
imgsz = 640                                     # Ukuran input image
conf_thres = 0.4                                # Confidence threshold
iou_thres = 0.45                                # IOU threshold

# === PERSIAPAN ===
device = select_device('')  # '' akan otomatis pakai CUDA jika tersedia
model = attempt_load(weights_path, map_location=device)  # Load model
model.eval()

names = model.names  # Kelas object

# === VIDEO CAPTURE ===
cap = cv2.VideoCapture(0)  # Gunakan path video jika tidak ingin webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert image ke tensor
    img = cv2.resize(frame, (imgsz, imgsz))
    img_tensor = torch.from_numpy(img).to(device)
    img_tensor = img_tensor.permute(2, 0, 1).float() / 255.0
    img_tensor = img_tensor.unsqueeze(0)

    # Inference
    with torch.no_grad():
        pred = model(img_tensor)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres)

    # Hasil deteksi
    det = pred[0]
    if det is not None and len(det):
        det[:, :4] = scale_coords(img_tensor.shape[2:], det[:, :4], frame.shape).round()

        for *xyxy, conf, cls in det:
            label = f'{names[int(cls)]} {conf:.2f}'
            xyxy = [int(x.item()) for x in xyxy]
            cv2.rectangle(frame, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
            cv2.putText(frame, label, (xyxy[0], xyxy[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Tampilkan hasil
    cv2.imshow('YOLOv7 Detection', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
