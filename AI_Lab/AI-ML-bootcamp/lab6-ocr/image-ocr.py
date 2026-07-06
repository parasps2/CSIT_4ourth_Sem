import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR


IMAGE_PATH = r"lab9-ocr\bill-img.jpg"

# ------------------------------------------------
# Load Image
# ------------------------------------------------

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise FileNotFoundError(f"Cannot load image: {IMAGE_PATH}")

# ------------------------------------------------
# Initialize OCR
# ------------------------------------------------

ocr = RapidOCR()

# ------------------------------------------------
# Run OCR
# ------------------------------------------------

result, _ = ocr(image)

if result is None:
    print("No text found.")
    exit()

# ------------------------------------------------
# Draw Results
# ------------------------------------------------

for item in result:

    # Print item to understand the structure
    print(item)

    # Handle different versions of RapidOCR
    if len(item) == 3:
        box, text, score = item
    else:
        continue

    pts = np.array(box, dtype=np.int32)

    cv2.polylines(
        image,
        [pts],
        True,
        (0, 255, 0),
        2
    )

    x = int(pts[0][0])
    y = int(pts[0][1])

    cv2.putText(
        image,
        text,
        (x, y - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

# ------------------------------------------------
# Show
# ------------------------------------------------

cv2.imshow("OCR Result", image)

cv2.imwrite("ocr_result.jpg", image)

print("Saved -> ocr_result.jpg")

cv2.waitKey(0)
cv2.destroyAllWindows()