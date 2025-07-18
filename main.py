import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

# Initialize hand detector
detector = HandDetector(detectionCon=0.5, maxHands=1)

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 600)
cap.set(4, 400)

# Timing to avoid key spam
lastActionTime = 0
cooldown = 0.2  # seconds

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)
    currentTime = time.time()

    if hands:
        fingers = detector.fingersUp(hands[0])
        totalFingers = fingers.count(1)

        cv2.putText(img, f'Fingers: {totalFingers}', (50, 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        if totalFingers == 5:
            pyautogui.keyDown('left')
            pyautogui.keyUp('right')
        
        elif totalFingers == 0:
            pyautogui.keyDown('right')
            pyautogui.keyUp('left')
        else:
            pyautogui.keyUp('up')
            pyautogui.keyUp('down')

    else:
        
        pyautogui.keyUp('up')
        pyautogui.keyUp('down')

    cv2.imshow('Camera Feed', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pyautogui.keyUp('up')
pyautogui.keyUp('down')
