import mediapipe as mp
import cv2
import math
import numpy as np
import os

Hands = mp.solutions.hands
Draw = mp.solutions.drawing_utils

from multiprocess import process as pc
import pyautogui

w, h = pyautogui.size()
screen = np.ones((h, w))


def ws():
    while True:
        cv2.imshow("white", screen)
        cv2.moveWindow("white", 0, 0)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyWindow("white")
            break


class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = Hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                 min_tracking_confidence=min_tracking_confidence)

    def findHandLandMarks(self, image, handNumber=0, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
        results = self.hands.process(image)
        landMarkList = []

        if results.multi_handedness:
            label = results.multi_handedness[handNumber].classification[0].label  # label gives if hand is left or right
            # account for inversion in cam
            if label == "Left":
                label = "Right"
            elif label == "Right":
                label = "Left"

        if results.multi_hand_landmarks:  # returns None if hand is not found
            hand = results.multi_hand_landmarks[
                handNumber]  # results.multi_hand_landmarks returns landMarks for all the hands

            for id, landMark in enumerate(hand.landmark):
                # landMark holds x,y,z ratios of single landmark
                imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
                xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                landMarkList.append([id, xPos, yPos, label])

            if draw:
                Draw.draw_landmarks(originalImage, hand, Hands.HAND_CONNECTIONS)

        return landMarkList


handDetector = HandDetector(min_detection_confidence=0.7)


def main():
    cam = cv2.VideoCapture(0)
    while True:
        status, image = cam.read()
        image = cv2.flip(image, 1)
        handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
        count = 0
        x = 0
        y = 0
        if (len(handLandmarks) != 0):
            # handLandmarks[point of 21 points][x or y] locates finger positions.
            # see details: https://google.github.io/mediapipe/solutions/hands
            # handLandmarks[4][1] 4->Thumb_tip 1->x-axis
            # handLandmarks[8][2] 8->Index_finger_tip 2->y-axis

            if handLandmarks[4][1] + 50 < handLandmarks[5][1]:  # Thumb finger
                count = count + 1
            if handLandmarks[8][2] < handLandmarks[6][2]:  # Index finger
                count = count + 1
            if handLandmarks[12][2] < handLandmarks[10][2]:  # Middle finger
                count = count + 1
            if handLandmarks[16][2] < handLandmarks[14][2]:  # Ring finger
                count = count + 1
            if handLandmarks[20][2] < handLandmarks[18][2]:  # Little finger
                count = count + 1
            x = handLandmarks[4][1]
            y = handLandmarks[4][2]
        cv2.putText(image, str(count), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 25)
        cv2.putText(image, "x=" + str(x), (25, 75), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        cv2.putText(image, "y=" + str(y), (25, 175), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
        cv2.imshow("result", image)
        cv2.moveWindow("result", 600, 400)
        cv2.setWindowProperty("result", cv2.WND_PROP_TOPMOST, 1)
        if cv2.waitKey(1) == ord('q'):
            cam.release()
            cv2.destroyWindow("result")
            break


if __name__ == '__main__':
    #p = pc.Process(target=ws)
    #p.start()
    main()
    #p.join()
    os._exit(0)