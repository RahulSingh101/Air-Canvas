import cv2

# Default color palette (BGR format)
COLOR_PALETTE = {
    "Red": (0, 0, 255),
    "Blue": (255, 0, 0),
    "Green": (0, 255, 0),
    "Yellow": (0, 255, 255),
    "White": (255, 255, 255)
}

def draw_top_bar(frame):
    """
    Draw the UI bar at the top of the screen with color selection buttons
    and the CLEAR button.
    """
    cv2.rectangle(frame, (0, 0), (640, 80), (40, 40, 40), -1)

    x = 10
    for color_name, bgr in COLOR_PALETTE.items():
        cv2.rectangle(frame, (x, 10), (x + 60, 60), bgr, -1)
        cv2.putText(frame, color_name[0], (x + 20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        x += 70

    # Clear Box
    cv2.rectangle(frame, (500, 10), (630, 60), (255, 255, 255), 2)
    cv2.putText(frame, "CLEAR", (520, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


def detect_color_selection(ix, iy):
    """
    Detect which palette color the user selected.
    Returns:
        (color_name, BGR tuple) OR (None, None)
    """
    x = 10
    for color_name, bgr in COLOR_PALETTE.items():
        if 10 < iy < 60 and x < ix < x + 60:
            return color_name, bgr
        x += 70

    return None, None


def detect_clear(ix, iy):
    """Check if user tapped the CLEAR button in the top-right corner."""
    return (500 < ix < 630) and (10 < iy < 60)
