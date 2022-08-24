import Tello_Keyboard as kp
from djitellopy import tello
from time import sleep
import numpy as np
import cv2
import math

######### Parameters ########
fspeed = 20 #cm/s
aspeed = 36 #deg/s
interval = 0.25

dInterval = fspeed*interval
aInterval = aspeed*interval
############################
x, y = 500,500
angle = 0
yaw = 0

points = [(0,0), (0,0)]

kp.init()

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

def getKeyInput():
    lr, fb, ud, yv = 0,0,0,0
    speed = 30
    angspeed = 50
    dist = 0
    global x, y, yaw, angle

    if kp.getKey("LEFT"):
        lr = -speed
        dist = dInterval
        angle = -180

    elif kp.getKey("RIGHT"):
        lr = speed
        dist = -dInterval
        angle = 180

    if kp.getKey("UP"):
        fb = speed
        dist = dInterval
        angle = 270
    elif kp.getKey("DOWN"):
        fb = -speed
        dist = -dInterval
        angle = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = angspeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = -angspeed
        yaw += aInterval

    if kp.getKey("e"):
        drone.takeoff()

    if kp.getKey("q"):
        drone.land()

    sleep(0.25)
    angle += yaw
    x += int(dist*math.cos(math.radians(angle)))
    y += int(dist*math.sin(math.radians(angle)))

    return [lr, fb, ud, yv, x, y]

def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0,0,255), cv2.FILLED)
    cv2.circle(img, points[-1], 10, (0,255,0), cv2.FILLED)
    cv2.putText(img, f"({(points[-1][0]-500)/100}, {(points[-1][1]-500)/100})m",
    (points[-1][0] + 10, points[-1][1] - 30), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 1)

while True:
    values = getKeyInput()
    drone.send_rc_control(values[0],values[1],values[2],values[3])

    img = np.zeros((1000,1000,3), np.uint8)
    if (points[-1][0] != values[4] or points[-1][1] != values[5]):
        points.append((values[4], values[5]))
    drawPoints(img, points)
    cv2.imshow("Map", img)
    cv2.waitKey(1)