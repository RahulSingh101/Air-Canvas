import cv2
import numpy as np
from utils.hand_tracking import HandTracker
from utils.gestures import GestureDetector

# Colors (BGR)
COLORS = {
    "Red": (0, 0, 255),
    "Blue": (255, 0, 0),
    "Green": (0, 255, 0),
    "Yellow": (0, 255, 255),
    "White": (255, 255, 255)
}

brush_color = COLORS["Red"]
brush_thickness = 10
eraser_thickness = 60

canvas = None
history = []  # for undo feature

cap = cv2.VideoCapture(0)
tracker = HandTracker()
gesture = GestureDetector()

def draw_ui(frame):
    """ Top bar UI """
    cv2.rectangle(frame, (0, 0), (640, 80), (50, 50, 50), -1)

    x = 10
    for color, bgr in COLORS.items():
        cv2.rectangle(frame, (x, 10), (x + 60, 60), bgr, -1)
        x += 70

    cv2.rectangle(frame, (500, 10), (630, 60), (255, 255, 255), 2)
    cv2.putText(frame, "CLEAR", (520, 45), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    # UI
    draw_ui(frame)

    # Hand Detection
    hand = tracker.find_hands(frame)
    index = tracker.get_finger_tip(frame, 8)
    middle = tracker.get_finger_tip(frame, 12)

    if index:
        ix, iy = index

        # COLOR PICKER
        if iy < 80:
            if 10 < ix < 70: brush_color = COLORS["Red"]
            elif 80 < ix < 140: brush_color = COLORS["Blue"]
            elif 150 < ix < 210: brush_color = COLORS["Green"]
            elif 220 < ix < 280: brush_color = COLORS["Yellow"]
            elif 290 < ix < 350: brush_color = COLORS["White"]
            elif 500 < ix < 630: canvas = np.zeros_like(frame)
        
        # Drawing
        if gesture.is_draw_mode():
            if tracker.prev_point is not None:
                cv2.line(canvas, tracker.prev_point, (ix, iy),
                         brush_color, brush_thickness)
            tracker.prev_point = (ix, iy)

        # Eraser
        elif gesture.is_erase_mode():
            if tracker.prev_point is not None:
                cv2.line(canvas, tracker.prev_point, (ix, iy),
                         (0, 0, 0), eraser_thickness)
            tracker.prev_point = (ix, iy)

        # Increase brush size
        elif gesture.is_zoom_in():
            brush_thickness = min(brush_thickness + 1, 50)

        # Decrease brush size
        elif gesture.is_zoom_out():
            brush_thickness = max(brush_thickness - 1, 1)

        # Undo gesture
        elif gesture.is_undo():
            if history:
                canvas = history.pop()

        else:
            tracker.prev_point = None

    # Save canvas state for undo
    history.append(canvas.copy())

    # Merge canvas & frame
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(canvas_gray, 20, 255, cv2.THRESH_BINARY)
    inv = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(frame, frame, mask=inv)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    final = cv2.add(frame_bg, canvas_fg)

    cv2.imshow("Air Canvas Advanced", final)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
