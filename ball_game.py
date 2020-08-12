import numpy as np
import cv2
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # print(ret, frame)
    thresh = cv2.inRange(hsv, (20, 70, 170), (40, 170, 255))

    st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21), (10, 10))
    st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11), (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, st1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, st2)
    thresh = cv2.GaussianBlur(thresh, (5, 5), 2)

    circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 2, 1, np.array([]), 80, 50, 5, 0)

    if circles.size != 0:
        # print(circles)
        maxRadius = 0
        x = 0
        y = 0
        found = False

        for c in circles[0]:
            found = True
            if c[2] > maxRadius:
                maxRadius = int(c[2])
                x = int(c[0])
                y = int(c[1])
        if found:
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
            cv2.circle(frame, (x, y), maxRadius, (255, 0, 0), 3)

            # x 0 - 640
            # y 0 - 480
            w = 'центр'
            if x > 426:
                w = 'лево'
                keyboard.press('a')
                # keyboard.release('a')
            elif x < 213:
                w = 'право'
                keyboard.press('d')
            else:
                w = 'центр'
                keyboard.release('d')
                keyboard.release('a')

                # keyboard.release('d')
            h = 'центр'
            if y > 320:
                h = 'низ'
                keyboard.press('s')
            elif y < 160:
                keyboard.press('k')
                h = 'верх'
            else:
                keyboard.release('k')
                keyboard.release('s')
            # print(w, '-', h)
            # print(x, y)

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GREEN)

    # Display the resulting frame
    # cv2.imshow('frame', thresh)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
