# YOLOv5 Object Detection — `deteksi.py`

Script ini menjalankan deteksi objek menggunakan YOLOv5 model yang sudah di-train.  
Kamera USB/webcam digunakan untuk mendeteksi benda (misal: tabung besi) secara realtime.

---

### Clone repo

```bash
git clone https://github.com/fafnir96/cylinder-object-robot.git
```

---

## 🖥️ Step by Step — Windows

### 1️⃣ Clone repo YOLOv5

```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
```

---

### 2️⃣ Buat virtual environment (venv)

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install dependencies YOLOv5

```bash
pip install -r requirements.txt
pip install opencv-python
```

---

### 4️⃣ Pastikan model best.pt sudah ada

```
runs/train/tabung_besi_v5n7/weights/best.pt
```

---

### 5️⃣ Jalankan deteksi.py

```bash
python deteksi.py
```

---

## 🚀 Step by Step — Jetson Nano

### 1️⃣ Clone YOLOv5

```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
```

---

### 2️⃣ Install PyTorch (pakai .whl sesuai JetPack)

Download wheel PyTorch di:  
[https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048)

Install:

```bash
pip install torch-xxx.whl
pip install torchvision-xxx.whl
```

---

### 3️⃣ Install dependencies YOLOv5

```bash
pip install -r requirements.txt
pip install opencv-python
```

---

### 4️⃣ Jalankan deteksi.py

```bash
python3 deteksi.py
```

---

## 🎥 deteksi.py

```python
import torch
import cv2

# Load YOLOv5 model
model = torch.hub.load('yolov5', 'custom', path='runs/train/tabung_besi_v5n7/weights/best.pt', source='local')
model.conf = 0.4

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    results.render()

    cv2.imshow('YOLOv5 Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 🗑️ Catatan

✅ Kamera USB support (720p / 1080p)  
✅ Webcam index `cv2.VideoCapture(0)` — kalau ada lebih dari 1 webcam, coba ubah `0` ke `1` atau `2`  
✅ Python 3.9 / 3.10 lebih aman  
✅ Model YOLOv5 hasil training pakai `train.py` YOLOv5

---
