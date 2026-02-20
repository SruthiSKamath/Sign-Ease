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

# Virtual keyboard layout
keyboard = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
    ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
    ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '?'],
    ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    ['SPACE', 'BS']
]

# Screen setup
screen_width = 1280
screen_height = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

button_size = 50
start_x, start_y = 50, 50
buttons = {}

for i, row in enumerate(keyboard):
    for j, key in enumerate(row):
        x = start_x + j * button_size
        y = start_y + i * button_size
        if key == 'SPACE':
            buttons[key] = (x, y, button_size * 6, button_size)
        elif key == 'BS':
            x = start_x + 6 * button_size
            buttons[key] = (x, y, button_size * 4, button_size)
        else:
            buttons[key] = (x, y, button_size, button_size)

typed_text = ""
last_pressed = None
press_time = 0
press_threshold = 0.5

# Moving average filter for finger position
position_history = deque(maxlen=5)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def draw_buttons(img):
    for key, (x, y, w, h) in buttons.items():
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Center text on button
        (text_w, text_h), _ = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        text_x = x + (w - text_w) // 2
        text_y = y + (h + text_h) // 2
        cv2.putText(img, key, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

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
            for key, (x, y, w, h) in buttons.items():
                if x < avg_cx < x + w and y < avg_cy < y + h:
                    if last_pressed == key:
                        if time.time() - press_time > press_threshold:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)

                            # Re-center text on pressed button
                            (text_w, text_h), _ = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                            text_x = x + (w - text_w) // 2
                            text_y = y + (h + text_h) // 2
                            cv2.putText(frame, key, (text_x, text_y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                            if key == "BS":
                                typed_text = typed_text[:-1]
                                speak("Backspace")
                            elif key == "SPACE":
                                typed_text += " "
                                speak("Space")
                            elif key == "?":
                                typed_text += "?"
                                speak("Question mark")
                            elif key == ".":
                                typed_text += "."
                                speak("Period")
                            elif key == ",":
                                typed_text += ","
                                speak("Comma")
                            else:
                                typed_text += key
                                speak(key)

                            last_pressed = None
                    else:
                        last_pressed = key
                        press_time = time.time()

    # Show typed text in dark magenta
    cv2.putText(frame, typed_text, (50, screen_height - 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (139, 0, 139), 2)

    cv2.imshow("Virtual Keyboard", frame)

    # Exit on ❌, q, or ESC
    if cv2.getWindowProperty("Virtual Keyboard", cv2.WND_PROP_VISIBLE) < 1:
        break
    key_pressed = cv2.waitKey(1) & 0xFF
    if key_pressed == ord('q') or key_pressed == 27:  # 27 = ESC
        break

# Release resources
cap.release()
hands.close()
cv2.destroyAllWindows()
