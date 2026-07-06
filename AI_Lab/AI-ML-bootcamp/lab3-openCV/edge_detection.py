import cv2

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    edges = cv2.Canny(frame,100,200)

    cv2.imshow("Edge Detection", edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()