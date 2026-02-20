import cv2
import mediapipe as mp
import random
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Game Variables
basket_x = 250  # Initial basket position
basket_width = 100
basket_height = 20
falling_obj_x = random.randint(50, 550)
falling_obj_y = 0
falling_speed = 5
score = 0

# OpenCV Window
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Hand tracking logic
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_pos = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * w)
            basket_x = max(50, min(x_pos, w - 50))  # Constrain within screen width

    # Update falling object
    falling_obj_y += falling_speed
    if falling_obj_y > h:
        falling_obj_x = random.randint(50, 550)
        falling_obj_y = 0

    # Collision detection
    if (basket_x - 50 < falling_obj_x < basket_x + 50) and (falling_obj_y + 20 > h - 50):
        score += 1
        falling_obj_y = 0
        falling_obj_x = random.randint(50, 550)

    # Draw basket
    cv2.rectangle(frame, (basket_x - 50, h - 50), (basket_x + 50, h - 50 + basket_height), (255, 0, 0), -1)
    
    # Draw falling object
    cv2.circle(frame, (falling_obj_x, falling_obj_y), 20, (0, 255, 0), -1)
    
    # Display score
    cv2.putText(frame, f'Score: {score}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Hand Gesture Game", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()