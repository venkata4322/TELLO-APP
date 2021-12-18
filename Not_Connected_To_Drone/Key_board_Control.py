from djitellopy import tello
import Key_Press_Module as kp
from time import sleep

kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

def getkeyboardInput():
    lr, fb, up,yv = 0, 0, 0, 0
    speed = 50

    if kp.getkey("LEFT"): lr = -speed
    elif kp.getkey("RIGHT"): lr = speed

    if kp.getkey("UP"): fb = speed
    elif kp.getkey("DOWN"): fb = -speed

    if kp.getkey("w"): ud = speed
    elif kp.getkey("s"): ud = -speed

    if kp.getkey("a"): yv = speed
    elif kp.getkey("d"): yv = -speed

    if kp.getkey("q"): yv = me.land()
    if kp.getkey("e"): yv = me.takeoff()

    return[lr, fb, ud,  yv]




me.takeoff()

while True:
    vals = getkeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)
