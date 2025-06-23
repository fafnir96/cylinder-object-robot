import torch
import cv2

# Load model (ganti path ke model hasil training kamu)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='runs/train/tabung_besi_v5n7/weights/best.pt', force_reload=True)

# Set confidence threshold
model.conf = 0.4  # bisa disesuaikan

# Open webcam (0 untuk webcam default)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame)

    # Render hasil ke frame
    results.render()

    # Tampilkan frame
    cv2.imshow('YOLOv5 Detection', frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
