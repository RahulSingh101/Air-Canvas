🖌️ Air Canvas using Python & Computer Vision
  Draw in the air using hand gestures — no physical tools required!

This project uses OpenCV, NumPy, and hand-tracking techniques to create a virtual drawing canvas that responds to your finger movements. Simply move your hand in front of the webcam and watch your sketches appear on screen in real time.

🚀 Features
    ✋ Hand/gesture detection using OpenCV
    🖍️ Draw in the air using your index finger
    🧼 Erase mode for clearing drawings
    🎨 Color selection (optional)
    📸 Real-time video processing
    💡 Simple, fast, and easy to use

🛠️ Technologies Used
    Python 3.x
    OpenCV
    NumPy
    Mediapipe

✋ Controls
    Gesture / Action	                           Description
    Draw	                             Index finger up, middle finger down
    Erase	                             Index + middle fingers up
    Select Color	                     Hover over top bar color button
    Clear Canvas	                     Hover over CLEAR button

🧠 How It Works
    The webcam captures frames in real time
    The program detects your hand using cv2 + Mediapipe
    The index finger landmark coordinates are extracted
    Movement of the index finger is tracked frame-to-frame
    A virtual canvas overlays the video feed
    Drawing occurs by connecting points traced by your finger

📝 Requirements
    Python 3.7+
    Webcam
    Good lighting for better hand detection

🔮 Future Improvements
    Add brush-size adjustment
    Add gesture-based undo/redo
    Add palm-based color selection
    Improve gesture classification with a model
