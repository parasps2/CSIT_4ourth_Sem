import os
import cv2
import fitz
import numpy as np
from rapidocr_onnxruntime import RapidOCR

# ==========================================
# Configuration
# ==========================================

PDF_PATH = r"lab9-ocr\sample.pdf"

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================
# OCR
# ==========================================

ocr = RapidOCR()

all_text = ""

# ==========================================
# Open PDF
# ==========================================

doc = fitz.open(PDF_PATH)

print(f"Pages : {len(doc)}")

# ==========================================
# Process Every Page
# ==========================================

for page_index in range(len(doc)):

    page = doc.load_page(page_index)

    # Render page at high quality
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

    img = np.frombuffer(pix.samples, dtype=np.uint8)

    img = img.reshape(pix.height, pix.width, pix.n)

    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Save original page
    cv2.imwrite(
        os.path.join(
            OUTPUT_DIR,
            f"page_{page_index+1}.png"
        ),
        img
    )

    # OCR
    result, _ = ocr(img)

    if result is None:
        continue

    all_text += f"\n========== PAGE {page_index+1} ==========\n"

    for box, text, score in result:

        all_text += text + "\n"

        pts = np.array(box, np.int32)

        cv2.polylines(
            img,
            [pts],
            True,
            (0,255,0),
            2
        )

        x = int(pts[0][0])
        y = int(pts[0][1])

        cv2.putText(
            img,
            text,
            (x,y-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,0,255),
            2
        )

    cv2.imwrite(
        os.path.join(
            OUTPUT_DIR,
            f"page_{page_index+1}_ocr.png"
        ),
        img
    )

# ==========================================
# Save Text
# ==========================================

with open(
    os.path.join(OUTPUT_DIR, "ocr_output.txt"),
    "w",
    encoding="utf8"
) as f:

    f.write(all_text)

print("\nFinished!")
print("Results saved in:", OUTPUT_DIR)