import cv2
from cvzone.HandTrackingModule import HandDetector
import pygame
import os
import time

# Set the correct path to your music folder
music_folder = r"C:\Users\khand\Desktop\music"

# Initialize pygame mixer
pygame.mixer.init()

# Load songs from the folder
songs = [f for f in os.listdir(music_folder) if f.endswith(".mp3")]

# Check if songs exist
if not songs:
    raise ValueError("No songs found in the 'music' directory. Please add .mp3 files.")

current_song = 0

# Load first song
pygame.mixer.music.load(os.path.join(music_folder, songs[current_song]))

# Setup webcam and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Track last action to prevent rapid repeats
last_action = ""
last_time = time.time()
cooldown = 1.0  # 1 second delay between actions

def change_song(index):
    """Change the currently playing song."""
    global current_song
    if 0 <= index < len(songs):
        current_song = index
        pygame.mixer.music.load(os.path.join(music_folder, songs[current_song]))
        pygame.mixer.music.play()

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        current_time = time.time()

        if fingers == [0, 1, 0, 0, 0] and last_action != "play" and current_time - last_time > cooldown:
            pygame.mixer.music.play()
            last_action = "play"
            last_time = current_time
            print("▶ Play")

        elif fingers == [0, 1, 1, 0, 0] and last_action != "pause" and current_time - last_time > cooldown:
            pygame.mixer.music.pause()
            last_action = "pause"
            last_time = current_time
            print("⏸ Pause")

        elif fingers == [0, 1, 1, 1, 0] and last_action != "next" and current_time - last_time > cooldown:
            current_song = (current_song + 
                            1) % len(songs)
            change_song(current_song)
            last_action = "next"
            last_time = current_time
            print("⏭ Next")

        elif fingers == [1, 0, 0, 0, 0] and last_action != "prev" and current_time - last_time > cooldown:
            current_song = (current_song - 1) % len(songs)
            change_song(current_song)
            last_action = "prev"
            last_time = current_time
            print("⏮ Previous")

    cv2.imshow("AI DJ", img)
    key = cv2.waitKey(1)
    if key == ord('q') or (hands and fingers == [1, 1, 1, 1, 1]): 
        pygame.mixer.music.stop()  # Stop music before closing
        break



cap.release()
cv2.destroyAllWindows()
