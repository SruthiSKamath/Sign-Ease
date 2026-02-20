import cv2
import mediapipe as mp
import pygame
import random
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Controlled Car Racing 🚗💨")

# Load assets
car_img = pygame.image.load("cars.jpg")  # Use a small car image (Replace with your path)
car_img = pygame.transform.scale(car_img, (160, 130))  # Resize

# Game Variables
car_x, car_y = WIDTH // 2 - 40, HEIGHT - 150
obstacle_x, obstacle_y = random.randint(100, WIDTH - 100), -100
obstacle_speed = 15
running = True

# MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Start video capture
cap = cv2.VideoCapture(0)

while running:
    screen.fill((0, 0, 0))  # Clear screen

    # Read webcam frame
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and process frame
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Hand detection
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = hand_landmarks.landmark
            hand_x = int(landmarks[8].x * WIDTH)  # Index finger tip position
            
            # Map hand position to car position
            car_x = np.clip(hand_x - 40, 100, WIDTH - 100)

            # Draw hand landmarks (Optional)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Move obstacle
    obstacle_y += obstacle_speed
    if obstacle_y > HEIGHT:
        obstacle_y = -100
        obstacle_x = random.randint(100, WIDTH - 100)

    # Collision detection
    if abs(car_x - obstacle_x) < 50 and abs(car_y - obstacle_y) < 80:
        print("Crash! Game Over!")
        running = False

    # Draw objects
    screen.blit(car_img, (car_x, car_y))
    pygame.draw.rect(screen, (255, 0, 0), (obstacle_x, obstacle_y, 60, 100))  # Obstacle

    # Refresh display
    pygame.display.flip()
    pygame.time.delay(30)  # Frame delay

    # Quit on pressing 'q'
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()
