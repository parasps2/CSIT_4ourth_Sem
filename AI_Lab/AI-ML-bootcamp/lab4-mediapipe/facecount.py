import cv2
import mediapipe as mp

mp_face = mp.solutions.face_detection
face_detector = mp_face.FaceDetection(model_selection=0)

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_detector.process(rgb)

    count = 0

    if results.detections:
        count = len(results.detections)

        for detection in results.detections:
            mp.solutions.drawing_utils.draw_detection(frame, detection)

    cv2.putText(frame,
                f"Faces: {count}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    cv2.imshow("Face Counter",frame)

    if cv2.waitKey(1)==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()