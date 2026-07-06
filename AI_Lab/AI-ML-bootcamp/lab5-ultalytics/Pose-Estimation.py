from ultralytics import YOLO
import cv2

model = YOLO("yolo11m-pose.pt")

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame)

    output = results[0].plot()

    cv2.imshow("Pose", output)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()