'''from djitellopy import tello
import cv2
import time

me = tello.Tello()
me.connect()
print(me.get_battery())


me.streamon()
face_cascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(1)
me.takeoff()
me.send_rc_control(0, 0, 5, 0)
time.sleep(2.2)
while True:
    _, img = me.get_frame_read().frame
    #_, img = cap.read()
    img = cv2.resize(img, (360, 240))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
'''

from djitellopy import tello
import cv2
import time

me = tello.Tello()
me.connect()
print(me.get_battery())


me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 5, 0)
time.sleep(2.2)
while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(1)