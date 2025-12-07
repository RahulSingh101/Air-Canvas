import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.drawer = mp.solutions.drawing_utils
        self.prev_point = None
        self.landmarks = None

    def find_hands(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        if result.multi_hand_landmarks:
            self.landmarks = result.multi_hand_landmarks[0]
            self.drawer.draw_landmarks(frame, self.landmarks,
                                       mp.solutions.hands.HAND_CONNECTIONS)
        else:
            self.landmarks = None
        
        return self.landmarks

    def get_finger_tip(self, frame, index):
        if not self.landmarks:
            return None
        h, w, _ = frame.shape
        x = int(self.landmarks.landmark[index].x * w)
        y = int(self.landmarks.landmark[index].y * h)
        return (x, y)
