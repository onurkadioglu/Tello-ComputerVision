import Tello_Keyboard as kp
from djitellopy import tello
from time import sleep



kp.init()

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

def getKeyInput():
    lr, fb, ud, yv = 0,0,0,0
    speed = 30

    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed

    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = speed
    elif kp.getKey("d"):
        yv = -speed

    if kp.getKey("e"):
        drone.takeoff()

    if kp.getKey("q"):
        drone.land()

    return [lr, fb, ud, yv]

#drone.takeoff()

while True:
    values = getKeyInput()
    drone.send_rc_control(values[0],values[1],values[2],values[3])
