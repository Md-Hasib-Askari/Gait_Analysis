import math
import time

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt
data_limit = 5000

pTime = time.time()
vpTime = pTime


# Class for Pose Detection
def velocity(detector, lmList_left, point):
    global pTime
    cTime = time.time() - pTime
    global vpTime
    vcTime = cTime - vpTime
    vpTime = cTime

    dict = {
        25: 'static/left_velocity.txt',
        26: 'static/right_velocity.txt',
    }
    if detector.prePos == detector.presentPos == [0, 0]:
        detector.presentPos = lmList_left[point][1:]
    else:
        detector.prePos = detector.presentPos
        detector.presentPos = lmList_left[point][1:]

    if detector.presentPos is not [0, 0]:
        distance = math.sqrt((detector.presentPos[0] - detector.prePos[0]) ** 2 +
                             (detector.presentPos[1] - detector.prePos[1]) ** 2)
        if vpTime > 0:
            vel = abs(distance) / vcTime
        else:
            return

        if len(open(dict[point], 'r').readlines()) > data_limit:
            open(dict[point], 'w').close()
        else:
            with open(dict[point], 'a') as file:
                file.write(str(cTime) + ',' + str(vel) + '\n')


def Point(point, lmList):
    dict = {
        23: 'static/left_position_hip.txt',
        25: 'static/left_position_knee.txt',
        27: 'static/left_position_ankle.txt',
        24: 'static/right_position_hip.txt',
        26: 'static/right_position_knee.txt',
        28: 'static/right_position_ankle.txt',
    }

    if len(open(dict[point], 'r').readlines()) > data_limit:
        open(dict[point], 'w').close()
    else:
        with open(dict[point], 'a') as file:
            x, y = lmList[point][1:]
            file.write(str(x) + ',' + str(y) + '\n')


def Angle(detector, img, p1, p2, p3, lmList):
    cTime = time.time()
    if p1 == 23:
        if len(open('static/left_angle.txt', 'r').readlines()) > data_limit:
            open('static/left_angle.txt', 'w').close()
        else:
            with open('static/left_angle.txt', 'a') as file:
                file.write(
                    str(cTime - pTime) + "," + str(detector.findAngle(img, p1, p2, p3, lmList, draw=False)) + '\n')
    elif p1 == 24:
        if len(open('static/right_angle.txt', 'r').readlines()) > data_limit:
            open('static/right_angle.txt', 'w').close()
        else:
            with open('static/right_angle.txt', 'a') as file:
                file.write(str(cTime - pTime) + "," + str(detector.findAngle(img, p1, p2, p3, lmList, draw=False)) +
                           '\n')


def start(ID):
    cap1 = cv2.VideoCapture("video.mp4")
    detector = PoseDetector()

    global pTime, vpTime
    pTime = time.time()
    vpTime = pTime


    while cap1.isOpened():
        success, img_left = cap1.read()

        if success:
            if img_left is None:
                continue
            # else:
            # img_left = cv2.resize(img_left, (640, 480))

            img_left = detector.findPose(img_left)
            lmList_left = detector.findPosition(img_left, draw=False)
            if len(lmList_left) != 0:
                # Angle --------------------------------
                # Left Leg
                if ID == 1:
                    Angle(detector, img_left, 24, 26, 28, lmList_left)
                # Right Leg
                if ID == 2:
                    Angle(detector, img_left, 23, 25, 27, lmList_left)

                # Point --------------------------------
                #  Left Leg
                if ID == 3:
                    Point(23, lmList_left)

                if ID == 4:
                    Point(25, lmList_left)

                if ID == 5:
                    Point(27, lmList_left)

                # # Right Leg
                if ID == 6:
                    Point(24, lmList_left)

                if ID == 7:
                    Point(26, lmList_left)

                if ID == 8:
                    Point(28, lmList_left)

                # Velocity --------------------------------
                # Left Leg
                if ID == 9:
                    velocity(detector, lmList_left, 25)
                # Right Leg
                if ID == 10:
                    velocity(detector, lmList_left, 26)

            # cv2.imshow("Image", img_left)
            cv2.waitKey(1)
        else:
            break

    cap1.release()
    cv2.destroyAllWindows()


class PoseDetector:
    prePos = [0, 0]
    presentPos = [0, 0]

    def __init__(self, mode=False, upBody=False, modelComplex=1, smooth=True, detectionCon=0.7, trackCon=0.7):
        self.mode = mode
        self.upBody = upBody
        self.modelComplex = modelComplex
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.results = None
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.modelComplex, self.smooth, self.detectionCon,
                                     self.trackCon)

    def findPose(self, img, draw=False):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=False):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList

    def findAngle(self, img, p1, p2, p3, lmList, draw=False):
        # Get the landmarks
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        x3, y3 = lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle < 0:
            angle += 360

        # Visualize the angle
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle


if __name__ == "__main__":
    detector = PoseDetector()
    start(1)
    print("Left Leg Angle Done.")
    start(2)
    print("Right Leg Angle Done.")
    start(3)
    print("Left Leg Hip Position Done.")
    start(4)
    print("Left Leg Knee Position Done.")
    start(5)
    print("Left Leg Ankle Position Done.")
    start(6)
    print("Right Leg Hip Position Done.")
    start(7)
    print("Right Leg Knee Position Done.")
    start(8)
    print("Right Leg Ankle Position Done.")
    start(9)
    print("Left Leg Velocity Done.")
    start(10)
    print("Left Leg Velocity Done.")
