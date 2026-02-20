import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=1)

# Function to calculate the Euclidean distance between two points
def calculate_distance(p1, p2):
    return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# Function to recognize hand gestures
def get_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    
    # Extract key points
    thumb_tip, thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_TIP], landmarks[mp_hands.HandLandmark.THUMB_IP]
    index_tip, index_mcp = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP], landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_tip, middle_mcp = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP], landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_tip, pinky_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP], landmarks[mp_hands.HandLandmark.PINKY_TIP]
    pinky_mcp = landmarks[mp_hands.HandLandmark.PINKY_MCP]
    fingers = [index_tip, middle_tip, ring_tip, pinky_tip]
    
    # 👍 Thumbs Up
    if thumb_tip.y < thumb_ip.y and all(f.y > middle_mcp.y for f in fingers):
        return "Like"
    
    # ✋ Open Palm (Universal Stop or Attention Signal)
    if all(f.y < middle_mcp.y for f in fingers) and thumb_tip.y < thumb_ip.y:
        return "Stop / Attention"
    
    # 🤞 Crossed Fingers (Request for Assistance)
    if index_tip.y < index_mcp.y and middle_tip.y < index_tip.y and all(f.y > middle_mcp.y for f in fingers[2:]):
        return "Need Assistance"
    
    # 👌 New OK Sign (Pinky and ring fingers up, others curled)
    if pinky_tip.y < pinky_mcp.y and ring_tip.y < middle_mcp.y and all(f.y > middle_mcp.y for f in [index_tip, middle_tip]):
        return "OK"
    
    # ☝️ Raised Index Finger (I Want Water)
    if index_tip.y < index_mcp.y and all(f.y > middle_mcp.y for f in fingers[1:]):
        return "I Want Water"
    
    # 🤙 Pinky Raised (I Want to Use the Washroom)
    if pinky_tip.y < pinky_mcp.y and all(f.y > middle_mcp.y for f in fingers[:3]):
        return "I Want to Use the Washroom"
    
    
    return "No Recognized Gesture"

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = get_gesture(hand_landmarks)
            cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Gesture Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()