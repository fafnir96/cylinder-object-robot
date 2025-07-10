import cv2
import torch
import serial
import time
import numpy as np

from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box
from models.experimental import attempt_load

# =============================
# Inisialisasi Model YOLOv7
# =============================

weights_path = 'runs/train/exp/weights/best.pt'  # Path model hasil training
img_size = 416
conf_thres = 0.4
iou_thres = 0.45

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = attempt_load(weights_path, map_location=device)
model.eval()

# =============================
# Inisialisasi Serial Robot
# =============================

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # ganti COM4

# =============================
# Fungsi Kontrol Robot
# =============================

def wait_complete_robot():
    while True:
        a = ser.readline()
        print(a.decode("utf-8"))
        if "ok" in a.decode("utf-8"):
            break

def calibrate():
    ser.write(b'G28\r')
    wait_complete_robot()

def nonlogam():
    ser.write(b'G0 X0.00 Y216.90 Z130.00 E130.00 F0.00\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y216.90 Z50.00 E130.00 F0.00\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y195.00 Z45.00 E130.00 F0.00\r')
    wait_complete_robot()
    ser.write(b'M6\r')
    wait_complete_robot()
    ser.write(b'M207\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y195.00 Z130.00 E130.00 F0.00\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y195.00 Z130.00 E0.00 F0.00\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'M7\r')
    wait_complete_robot()
    ser.write(b'M206\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y216.90 Z130.00 E0.00 F0.00\r')
    wait_complete_robot()

def logam():
    ser.write(b'G0 X0.00 Y216.90 Z130.00 E309.00 F0.00\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y216.90 Z50.00 E309.00 F0.00\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y195.00 Z45.00 E309.00 F0.00\r')
    wait_complete_robot()
    ser.write(b'M6\r')
    wait_complete_robot()
    ser.write(b'M207\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y200.00 Z130.00 E309.00 F0.00\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y195.00 Z130.00 E0.00 F0.00\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'M7\r')
    wait_complete_robot()
    ser.write(b'M206\r')
    wait_complete_robot()
    time.sleep(1)
    ser.write(b'G0 X0.00 Y216.90 Z130.00 E0.00 F0.00\r')
    wait_complete_robot()

# =============================
# Fungsi Deteksi Cylinder
# =============================

def detect_cylinder(frame):
    img = letterbox(frame, img_size, stride=32, auto=False)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(device).float() / 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img)[0]
    pred = non_max_suppression(pred, conf_thres, iou_thres)[0]

    if pred is not None and len(pred):
        pred[:, :4] = scale_coords(img.shape[2:], pred[:, :4], frame.shape).round()
        for *xyxy, conf, cls in pred:
            label = int(cls.item())
            if label == 0:  # Label 0 diasumsikan cylinder
                plot_one_box(xyxy, frame, label='Cylinder', color=(255, 0, 0), line_thickness=2)
                return True
    return False

# =============================
# Main Program
# =============================

calibrate()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if detect_cylinder(frame):
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print("Serial Data:", line)
            if "LOGAM" in line:
                logam()
            elif "NON" in line:
                nonlogam()

    cv2.imshow('Deteksi', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()