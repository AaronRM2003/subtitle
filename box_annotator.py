import cv2
import numpy as np
import json
import requests

# =====================
# CONFIG
# =====================
IMAGE_URL = "https://img.youtube.com/vi/T50vk3-iz-w/maxresdefault.jpg"
OUTPUT_JSON = "output_boxes.json"

BOXES = []
TEXTS = {
    "en": []
}

drawing = False
ix, iy = -1, -1
current_box = None

mode = "draw_box"  # draw_box | pick_bg | pick_font
bg_color = None
font_color = None

# =====================
# LOAD IMAGE
# =====================
response = requests.get(IMAGE_URL)
image = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)
clone = image.copy()
h, w = image.shape[:2]

# =====================
# COLOR UTILS
# =====================
def bgr_to_hex(bgr):
    return "#{:02x}{:02x}{:02x}".format(int(bgr[2]), int(bgr[1]), int(bgr[0]))

def draw_color_preview(img, bg, font):
    if bg:
        cv2.rectangle(img, (10, h - 60), (110, h - 10), bg, -1)
        cv2.putText(img, "BG", (35, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    if font:
        cv2.rectangle(img, (130, h - 60), (230, h - 10), font, -1)
        cv2.putText(img, "FONT", (145, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

# =====================
# MOUSE CALLBACK
# =====================
def mouse_handler(event, x, y, flags, param):
    global ix, iy, drawing, image, current_box
    global mode, bg_color, font_color

    # DRAW BOX
    if mode == "draw_box":
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            temp = image.copy()
            cv2.rectangle(temp, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Annotator", temp)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            x0, y0 = min(ix, x), min(iy, y)
            x1, y1 = max(ix, x), max(iy, y)
            current_box = (x0, y0, x1 - x0, y1 - y0)
            mode = "pick_bg"

    # PICK BACKGROUND COLOR
    elif mode == "pick_bg" and event == cv2.EVENT_LBUTTONDOWN:
        bg_color = clone[y, x].tolist()
        mode = "pick_font"
        print("Background color selected:", bgr_to_hex(bg_color))

    # PICK FONT COLOR
    elif mode == "pick_font" and event == cv2.EVENT_LBUTTONDOWN:
        font_color = clone[y, x].tolist()
        print("Font color selected:", bgr_to_hex(font_color))

# =====================
# WINDOW
# =====================
cv2.namedWindow("Annotator")
cv2.setMouseCallback("Annotator", mouse_handler)

print("""
Controls:
- Draw box with mouse
- Click 1x → Background color
- Click 1x → Font color
- n = confirm box
- c = clear current box
- q = quit & save
""")

# =====================
# MAIN LOOP
# =====================
while True:
    display = image.copy()

    # Draw current box
    if current_box:
        x, y, bw, bh = current_box
        cv2.rectangle(display, (x, y), (x + bw, y + bh), (0, 255, 0), 2)

    # Draw color preview
    draw_color_preview(display, bg_color, font_color)

    cv2.imshow("Annotator", display)
    key = cv2.waitKey(1) & 0xFF

    # CLEAR
    if key == ord('c'):
        image = clone.copy()
        current_box = None
        bg_color = None
        font_color = None
        mode = "draw_box"
        print("Cleared current box")

    # CONFIRM
    # CONFIRM
    elif key == ord('n') and current_box and bg_color and font_color:
        x, y, bw, bh = current_box

        # Ask for text in terminal
        cv2.imshow("Annotator", display)
        cv2.waitKey(1)

        text = input("Enter text for this box (EN): ").strip()

        BOXES.append({
            "x": x,
            "y": y,
            "w": bw,
            "h": bh,
            "background": bgr_to_hex(bg_color),
            "fontColor": bgr_to_hex(font_color)
        })

        TEXTS["en"].append(text)

        print("Box + text saved")

        current_box = None
        bg_color = None
        font_color = None
        mode = "draw_box"

    # QUIT
    elif key == ord('q'):
        break

cv2.destroyAllWindows()

# =====================
# SAVE JSON
# =====================
output = {
    "boxes": BOXES,
    "texts": TEXTS
}

with open(OUTPUT_JSON, "w") as f:
    json.dump(output, f, indent=2)

print("\nSaved to", OUTPUT_JSON)
