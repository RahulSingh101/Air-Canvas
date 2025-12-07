import cv2
import numpy as np
from utils.hand_tracking import HandTracker
from utils.gestures import GestureDetector
from src.ui import draw_top_bar, detect_color_selection, detect_clear

# Initialize variables
brush_color = (0, 0, 255)  # Default Red
brush_thickness = 10
eraser_thickness = 60
canvas = None
history = []

# Initialize webcam, hand tracker, and gesture detector
cap = cv2.VideoCapture(0)
tracker = HandTracker()
gesture = GestureDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Draw UI at top
    draw_top_bar(frame)

    # Hand detection
    hand = tracker.find_hands(frame)
    index = tracker.get_finger_tip(frame, 8)
    middle = tracker.get_finger_tip(frame, 12)

    if index:
        ix, iy = index

        # Check for color selection
        color_name, color_bgr = detect_color_selection(ix, iy)
        if color_bgr:
            brush_color = color_bgr

        # Check for clear button
        if detect_clear(ix, iy):
            canvas = np.zeros_like(frame)
            history = []

        # Drawing
        if gesture.is_draw_mode():
            if tracker.prev_point is not None:
                cv2.line(canvas, tracker.prev_point, (ix, iy), brush_color, brush_thickness)
            tracker.prev_point = (ix, iy)

        # Eraser
        elif gesture.is_erase_mode():
            if tracker.prev_point is not None:
                cv2.line(canvas, tracker.prev_point, (ix, iy), (0, 0, 0), eraser_thickness)
            tracker.prev_point = (ix, iy)

        # Brush size increase/decrease
        elif gesture.is_zoom_in():
            brush_thickness = min(brush_thickness + 1, 50)
        elif gesture.is_zoom_out():
            brush_thickness = max(brush_thickness - 1, 1)

        # Undo
        elif gesture.is_undo():
            if history:
                canvas = history.pop()

        else:
            tracker.prev_point = None

    # Save canvas state for undo
    history.append(canvas.copy())

    # Merge canvas with webcam feed
    canvas_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(canvas_gray, 20, 255, cv2.THRESH_BINARY)
    inv_mask = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(frame, frame, mask=inv_mask)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    combined = cv2.add(frame_bg, canvas_fg)

    cv2.imshow("Air Canvas Advanced", combined)

    # Exit on ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
