import cv2
import numpy as np
from ultralytics import SAM

# =====================================================
# CONFIG
# =====================================================

IMAGE_PATH = r"lab7-sam2\doggy.jpg"
MODEL_PATH = "sam2.1_b.pt"

# Display scale (change as needed)
SCALE = 0.25    # 0.25 = 25%, 0.5 = 50%, 0.75 = 75%

# =====================================================
# LOAD MODEL
# =====================================================

model = SAM(MODEL_PATH)

img = cv2.imread(IMAGE_PATH)

if img is None:
    raise Exception("Image not found.")

original = img.copy()

h, w = original.shape[:2]

display = cv2.resize(
    original,
    (int(w * SCALE), int(h * SCALE)),
    interpolation=cv2.INTER_AREA
)

points = []
labels = []

# =====================================================
# MOUSE CALLBACK
# =====================================================

def mouse(event, x, y, flags, param):

    global display

    # Convert display coordinate -> original image coordinate
    ox = int(x / SCALE)
    oy = int(y / SCALE)

    ox = max(0, min(ox, w - 1))
    oy = max(0, min(oy, h - 1))

    # Foreground
    if event == cv2.EVENT_LBUTTONDOWN:

        points.append([ox, oy])
        labels.append(1)

        cv2.circle(display, (x, y), 5, (0, 255, 0), -1)

    # Background
    elif event == cv2.EVENT_RBUTTONDOWN:

        points.append([ox, oy])
        labels.append(0)

        cv2.circle(display, (x, y), 5, (0, 0, 255), -1)


# =====================================================
# WINDOW
# =====================================================

cv2.namedWindow("SAM2", cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback("SAM2", mouse)

print("""
============================================

Left Click   : Foreground Point
Right Click  : Background Point

S : Segment & Remove Background
R : Reset
ESC : Exit

============================================
""")

# =====================================================
# MAIN LOOP
# =====================================================

while True:

    cv2.imshow("SAM2", display)

    key = cv2.waitKey(1) & 0xFF

    # Exit
    if key == 27:
        break

    # Reset
    elif key == ord("r"):

        points.clear()
        labels.clear()

        display = cv2.resize(
            original,
            (int(w * SCALE), int(h * SCALE)),
            interpolation=cv2.INTER_AREA
        )

        print("Reset")

    # Segment
    elif key == ord("s"):

        if len(points) == 0:
            print("Please click on the image first.")
            continue

        print("Running SAM2...")

        results = model(
            IMAGE_PATH,
            points=[points],
            labels=[labels]
        )

        if results[0].masks is None:
            print("No object found.")
            continue

        mask = results[0].masks.data[0].cpu().numpy()
        mask = (mask > 0.5).astype(np.uint8)

        # --------------------------------------------
        # Transparent PNG
        # --------------------------------------------

        rgba = cv2.cvtColor(original, cv2.COLOR_BGR2BGRA)
        rgba[:, :, 3] = mask * 255

        cv2.imwrite("removed_bg.png", rgba)

        # --------------------------------------------
        # White Background Preview
        # --------------------------------------------

        preview = np.full_like(original, 255)
        preview[mask == 1] = original[mask == 1]

        preview_small = cv2.resize(
            preview,
            (int(w * SCALE), int(h * SCALE)),
            interpolation=cv2.INTER_AREA
        )

        cv2.imshow("Result", preview_small)

        print("Saved: removed_bg.png")

cv2.destroyAllWindows()