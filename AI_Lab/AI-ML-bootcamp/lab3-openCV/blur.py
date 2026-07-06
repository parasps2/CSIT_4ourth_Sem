import cv2

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    blur = cv2.GaussianBlur(frame,(15,15),0)

    cv2.imshow("Blur Camera", blur)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()