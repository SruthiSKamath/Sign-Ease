import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
from collections import deque

# Initialize text-to-speech
engine = pyttsx3.init()

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Virtual keyboard layout (Fit all numbers in the screen)
keyboard = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'BS'],
    ['+', '-', '*', '/', '=', 'C']
]

# Button configurations
button_size = 80  # Adjusted button size
start_x, start_y = 100, 250  # Adjusted for horizontal alignment
spacing = 10  # Space between buttons
buttons = {}

# Define button positions
for i, row in enumerate(keyboard):
    for j, key in enumerate(row):
        x = start_x + j * (button_size + spacing)
        y = start_y + i * (button_size + spacing)
        buttons[key] = (x, y)

calc_input = ""
last_pressed = None
press_time = 0
press_threshold = 0.5  # Require 0.5 seconds of continuous press

# Moving average filter for finger position
position_history = deque(maxlen=5)  # Store last 5 positions

def speak(text):
    engine.say(text)
    engine.runAndWait()

def draw_buttons(img):
    """Draw the virtual buttons on the screen with proper colors."""
    for key, (x, y) in buttons.items():
        text_color = (0, 0, 255) if key.isdigit() else (255, 0, 0)  # Red for numbers, blue for symbols
        cv2.rectangle(img, (x, y), (x + button_size, y + button_size), (0, 0, 0), 3)
        cv2.putText(img, key, (x + 20, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, text_color, 3)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    frame = cv2.resize(frame, (1200, 700))  # Resize the frame to a medium size
    draw_buttons(frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            # Smooth finger position
            position_history.append((cx, cy))
            avg_cx, avg_cy = np.mean(position_history, axis=0).astype(int)

            # Detect button press with stabilization
            for key, (x, y) in buttons.items():
                if x < avg_cx < x + button_size and y < avg_cy < y + button_size:
                    if last_pressed == key:
                        if time.time() - press_time > press_threshold:
                            cv2.rectangle(frame, (x, y), (x + button_size, y + button_size), (0, 255, 0), -1)
                            cv2.putText(frame, key, (x + 20, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

                            if key == "=":
                                try:
                                    calc_input = str(eval(calc_input))
                                    speak(calc_input)
                                except:
                                    calc_input = "Error"
                                    speak("Error")
                            elif key == "C":  # Clear button functionality
                                calc_input = ""
                                speak("Cleared")
                            elif key == "BS":  # Backspace functionality
                                calc_input = calc_input[:-1]
                                speak("Backspace")
                            else:
                                calc_input += key
                                speak(key)
                            
                            last_pressed = None  # Reset press tracking
                    else:
                        last_pressed = key
                        press_time = time.time()

    # Display current calculation
    cv2.rectangle(frame, (100, 50), (1100, 150), (0, 0, 0), -1)  # Black background for display
    cv2.putText(frame, calc_input, (120, 130), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.imshow("Virtual Keyboard Calculator", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
