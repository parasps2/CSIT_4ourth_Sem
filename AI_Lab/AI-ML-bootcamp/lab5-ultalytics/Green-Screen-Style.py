from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLO11 Segmentation model
model = YOLO("yolo11m-seg.pt")

cap = cv2.VideoCapture(0)

# Set webcam resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:

    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    # Green background
    green_bg = np.zeros((h, w, 3), dtype=np.uint8)
    green_bg[:] = (0, 255, 0)   # BGR

    results = model(frame, verbose=False)

    final_mask = np.zeros((h, w), dtype=np.uint8)

    if results[0].masks is not None:

        masks = results[0].masks.data.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()

        for mask, cls in zip(masks, classes):

            # Keep only person
            if int(cls) != 0:
                continue

            # Resize mask to image size
            mask = cv2.resize(mask, (w, h))

            mask = (mask > 0.5).astype(np.uint8)

            final_mask = np.maximum(final_mask, mask)

    # Copy person to green background
    output = green_bg.copy()
    output[final_mask == 1] = frame[final_mask == 1]

    cv2.imshow("Original", frame)
    cv2.imshow("Green Screen", output)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()