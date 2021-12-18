import cv2
import mediapipe as mp
import time
import numpy as np
from djitellopy import Tello


class FaceDetector():
    def __init__(self, minDetectionCon=0.5):

        self.minDetectionCon = minDetectionCon

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, image, me, draw=True):
        fbRange = [110, 125]
        w, h = 640, 480
        pid = [0.4, 0.4, 0]
        pError = 0

        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        # print(self.results)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = image.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
                #print(len(bboxs))                                    #length of box

                #area=int(bboxC.width * iw) * int(bboxC.height * ih)  #finding area if square
                fb = 0


                error=(int(bboxC.xmin * iw) - iw//2.5)//2
                #print(error)
                speed = pid[0] * error + pid[1] * (error - pError)
                speed = int(np.clip(speed, -100, 100))
                if int(bboxC.width * iw) > fbRange[0] and int(bboxC.width * iw)< fbRange[1]:
                    fb = 0
                elif int(bboxC.width * iw) > fbRange[1]:
                    fb = -20
                elif int(bboxC.width * iw) < fbRange[0] and int(bboxC.width * iw)!= 0:
                    fb = 20
                if len(bboxs)!= 1:
                    speed = 0
                    error = 0
                print(speed, fb)
                me.send_rc_control(0, fb, 0, speed)



                if draw:
                    image = self.fancyDraw(image,bbox)

                    cv2.putText(image, f'{int(detection.score[0] * 100)}%',
                            (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 2)


        return image, bboxs

    def fancyDraw(self, image, bbox, l=30, t=5, rt= 1):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        cv2.rectangle(image, bbox, (255, 0, 255), rt)
        # Top Left  x,y
        cv2.line(image, (x, y), (x + l, y), (255, 0, 255), t)
        cv2.line(image, (x, y), (x, y+l), (255, 0, 255), t)
        # Top Right  x1,y
        cv2.line(image, (x1, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(image, (x1, y), (x1, y+l), (255, 0, 255), t)
        # Bottom Left  x,y1
        cv2.line(image, (x, y1), (x + l, y1), (255, 0, 255), t)
        cv2.line(image, (x, y1), (x, y1 - l), (255, 0, 255), t)
        # Bottom Right  x1,y1
        cv2.line(image, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv2.line(image, (x1, y1), (x1, y1 - l), (255, 0, 255), t)
        return image

def telloGetFrame(me, w=640, h=480):
    myFrame = me.get_frame_read()
    myFrame = myFrame.frame
    image = cv2.resize(myFrame, (w, h))
    return image
def main():
    w, h = 640, 480
    me = Tello()
    me.connect()
    print(me.get_battery())

    me.streamon()

    me.takeoff()
    #me.send_rc_control(0, 0,10, 0)
    #cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()
    while True:
        #success, image = cap.read()
        image = telloGetFrame(me, w, h)
        img, bboxs = detector.findFaces(image,me)
        print(list(bboxs))

        '''cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)'''
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()