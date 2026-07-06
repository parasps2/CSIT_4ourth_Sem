from ultralytics import YOLO
import cv2

model = YOLO("yolo11m.pt")

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.track(frame, persist=True)

    output = results[0].plot()

    cv2.imshow("Tracking", output)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()
