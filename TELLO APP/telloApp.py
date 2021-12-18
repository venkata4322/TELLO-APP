from kivy import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.uix.camera import Camera
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.camera import Camera
import time
import logging
import FaceTracking
from pyUtils import timePrint, startThread
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from djitellopy import tello
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from pyzbar.pyzbar import decode
from kivy.lang import Builder
import numpy as np
import math
import widget
import cv2
import os
import threading
import datetime
import mediapipe as mp
from pyUtils import timePrint, timestamp
from pathlib import Path, PurePath

Builder.load_string("""
<KivyCamera>:
    FloatLayout:
        Button:
            id: forward
            pos_hint: {'x': 6.5, 'y': 1.5}
            size_hint: .5, .5
            on_press: root.on_move_forward()
            on_release: root.off_move_forward()
            background_normal: 'Resources/img/icons8-collapse-arrow-50.png'
            background_down: 'Resources/img/icons8-collapse-arrow-50-down.png'
        Button:
            pos_hint: {'x': 6.5, 'y': .5}
            size_hint: .5, .5
            on_press: root.on_move_backward()
            on_release: root.off_move_backward()
            background_normal: 'Resources/img/icons8-expand-arrow-50.png'
            background_down: 'Resources/img/icons8-expand-arrow-50-down.png'
        Button:
            pos_hint: {'x': 7, 'y': 1}
            size_hint: .5, .5
            on_press: root.on_move_right()
            on_release: root.off_move_right()
            background_normal: 'Resources/img/icons8-forward-50.png'
            background_down: 'Resources/img/icons8-forward-50-down.png'
        Button:
    	    pos_hint: {'x': 6, 'y': 1}
    	    size_hint: .5, .5
    	    on_press: root.on_move_left()
            on_release: root.off_move_left()
            background_normal: 'Resources/img/icons8-back-50.png'
            background_down: 'Resources/img/icons8-back-50-down.png'
        Button:
    	    pos_hint: {'x': 5.2, 'y': 0.5}
    	    size_hint: .5, .5
    	    on_press: root.on_Video_recorder()
            on_release: root.off_Video_recorder()
            background_normal: 'Resources/img/Video_recorder.jpeg'
            #background_down: 'Resources/img/icons8-back-50-down.png'
    	Button:
    	    pos_hint: {'x': 1, 'y': 1.5}
    	    size_hint: .5, .5
    	    on_press: root.on_move_up()
            on_release: root.off_move_up()
            background_normal: 'Resources/img/icons8-double-up-50.png'
            background_down: 'Resources/img/icons8-double-up-50-down.png'
    	Button:
    	    pos_hint: {'x': 1, 'y': .5}
    	    size_hint: .5, .5
    	    on_press: root.on_move_down()
            on_release: root.off_move_down()
            background_normal: 'Resources/img/icons8-double-down-50.png'
            background_down: 'Resources/img/icons8-double-down-50-down.png'
    	Button:
    	    pos_hint: {'x': 1.5, 'y': 1}
    	    size_hint: .5, .5
    	    on_press: root.on_move_rotateR()
            on_release: root.off_move_rotateR()
            background_normal: 'Resources/img/icons8-u-turn-to-right-50.png'
            background_down: 'Resources/img/icons8-u-turn-to-right-50-down.png'
        Button:
    	    pos_hint: {'x': 2.3, 'y': 0.5}
    	    size_hint: .5, .5
    	    on_press: root.on_capture_image()
            on_release: root.off_capture_image()
            background_normal: 'Resources/img/Image-Capture.jpeg'
            #background_down: 'Resources/img/icons8-u-turn-to-right-50-down.png'
    	Button:
    	    pos_hint: {'x': 0.5, 'y': 1}
    	    size_hint: .5, .5
    	    on_press: root.on_move_rotateL()
            on_release: root.off_move_rotateL()
            background_normal: 'Resources/img/icons8-u-turn-to-left-50.png'
            background_down: 'Resources/img/icons8-u-turn-to-left-50-down.png'
    	Button:
    	    pos_hint: {'x': 3.4, 'y': 0.5}
    	    size_hint: .5, .5
    	    on_press: root.takeoff()
    	    background_normal: 'Resources/img/outline_flight_takeoff_black_48dp.png'
    	    background_down: 'Resources/img/outline_flight_takeoff_black_48dp-down.png'
    	Button:
    	    pos_hint: {'x': 4.1, 'y': 0.5}
    	    size_hint: .5, .5
    	    on_press: root.land()
    	    background_normal: 'Resources/img/outline_flight_land_black_48dp.png'
    	    background_down: 'Resources/img/outline_flight_land_black_48dp-down.png'
    	Button:
    	    pos_hint: {'x': 3.2, 'y': 1.1}
    	    size_hint: .7, .5
    	    on_press: root.throwfly()
    	    color: 1, 1, 1, 1
    	    background_color: 0.1, 0.5, 0.6, 1
    	    text: "START"
    	Button:
    	    pos_hint: {'x': 4.1, 'y': 1.1}
    	    size_hint: .7, .5
    	    on_press: root.motoron()
    	    color: 1, 1, 1, 1
    	    background_color: 0.1, 0.5, 0.6, 1
    	    text: "STOP"
    	Label:
    	    id: battery_label
    	    text: 'Battery: 0%'
    	    color: 1, 1, 1, 1
    	    background_color: 0.1, 0.5, 0.6, 1
    	    text_size: 400, None
    	    pos: 160, 530
    	    canvas.before:
    	        Color:
    	            rgba: self.background_color
    	        Rectangle:
    	            size: 110, 40
    	            pos: 0, 560
    	Label:
    	    id: temperature_label
    	    text: 'Temperature: 0°C'
    	    color: 1, 1, 1, 1
    	    background_color: 0.1, 0.5, 0.6, 1
    	    text_size: 400, None
    	    pos: 275, 530
    	    canvas.before:
    	        Color:
    	            rgba: self.background_color
    	        Rectangle:
    	            size: 155, 40
    	            pos: 120, 560
    	Label:
    	    id: barometer_label
    	    text: 'Altitude: 0cm'
    	    color: 1, 1, 1, 1
    	    background_color: 0.1, 0.5, 0.6, 1
    	    text_size: 400, None
    	    pos: 440, 530
    	    canvas.before:
    	        Color:
    	            rgba: self.background_color
    	        Rectangle:
    	            size: 115, 40
    	            pos: 285, 560
    	Label:
    	    id: time_flight_label
    	    text: 'Flight Time: 0s'
    	    color: 1, 1, 1, 1
    	    background_color: 0.1, 0.5, 0.6, 1
    	    text_size: 400, None
    	    pos: 570, 530
    	    canvas.before:
    	        Color:
    	            rgba: self.background_color
    	        Rectangle:
    	            size: 135, 40
    	            pos: 410, 560
    	Label:
    	    id: not_connected
    	    text: 'Please Connect The Drone Before Running The App'
    	    color: 1, 0, 0, 1
    	    text_size: 500, None
    	    pos: 350, 350
    	BoxLayout:
    	    orientation: 'vertical'
    	    width: 120 if root.dropdown.isShowFlipButton else 0
    	    height: 120
    	    pos: 0, 300
    	    size_hint: None, 1
    	    opacity: 1 if root.dropdown.isShowFlipButton else 0
    	    display: 'inline-block'
    	    Button:
    	        text: 'Flip Right'
    	        on_press: root.flip("r")
    	    Button:
    	        text: 'Flip Left'
    	        on_press: root.flip("l")
    	    Button:
    	        text: 'Flip Forward'
    	        on_press: root.flip("f")
    	    Button:
    	        text: 'Flip Backward'
    	        on_press: root.flip("b")
    	        

<CustomDropDown>:
    Button:
        text: 'Flip Mod'
        size_hint_y: None
        height: 44
        on_press: root.isShowFlipButton = not root.isShowFlipButton
        background_color: (1, .3, .4, .85) if root.isShowFlipButton else (1, .3, .4, .85)
    Button:
        text: 'FaceTracking'
        size_hint_y: None
        height: 44
        on_press: root.isFaceTracking = not root.isFaceTracking
        background_color: (1, .3, .4, .85) if root.isFaceTracking else (1, .3, .4, .85)
    Button:
        text: 'QrCode Action'
        size_hint_y: None
        height: 44
        on_press: root.isQrCodeAction = not root.isQrCodeAction
        background_color: (1, .3, .4, .85) if root.isQrCodeAction else (1, .3, .4, .85)
    Button:
        text: '360 Mod'
        size_hint_y: None
        height: 44
        on_press: root.isRoundMod = not root.isRoundMod
        background_color: (1, .3, .4, .85) if root.isRoundMod else (1, .3, .4, .85)
    Button:
        text: 'Rebound Mod'
        size_hint_y: None
        height: 44
        on_press: root.isReboundMod = not root.isReboundMod
        background_color: (1, .3, .4, .85) if root.isReboundMod else (1, .3, .4, .85)
    Button:
        text: 'Big Angle'
        size_hint_y: None
        height: 44
        on_press: root.isBigAngle = not root.isBigAngle
        background_color: (1, .3, .4, .85) if root.isBigAngle else (1, .3, .4, .85)
""")

        #Builder.load_file('tello.kv')


class CustomDropDown(DropDown):
    isShowFlipButton = BooleanProperty(False)
    isFaceTracking = BooleanProperty(False)
    isQrCodeAction = BooleanProperty(False)
    isRoundMod = BooleanProperty(False)
    isReboundMod = BooleanProperty(False)
    isBigAngle = BooleanProperty(False)


def circle(radius: int, direction: str, rotation: str, inclinaison: int, speed: int,
           tello):

    assert radius >= 50;"Le rayon du cercle doit être supérieur à 50 cm"
    assert -90 <= inclinaison <= 90, "L'inclinaison doit être comprise entre -90 et 90"

    z = math.cos(inclinaison / 90) * radius
    if inclinaison < 0:
        z *= -1
    if direction == 'avant':
        if rotation == 'cw':
            tello.curve_xyz_speed(x1=radius, y1=radius, z1=int(z), x2=2 * radius, y2=0, z2=0, speed=speed)
            tello.curve_xyz_speed(x1=-radius, y1=-radius, z1=int(-z), x2=-2 * radius, y2=0, z2=0, speed=speed)
        if rotation == 'ccw':
            tello.curve_xyz_speed(x1=radius, y1=-radius, z1=int(z), x2=2 * radius, y2=0, z2=0, speed=speed)
            tello.curve_xyz_speed(x1=-radius, y1=radius, z1=int(-z), x2=-2 * radius, y2=0, z2=0, speed=speed)
    if direction == 'arriere':
        if rotation == 'cw':
            tello.curve_xyz_speed(x1=-radius, y1=-radius, z1=int(z), x2=-2 * radius, y2=0, z2=0, speed=speed)
            tello.curve_xyz_speed(x1=radius, y1=radius, z1=int(-z), x2=2 * radius, y2=0, z2=0, speed=speed)
        if rotation == 'ccw':
            tello.curve_xyz_speed(x1=-radius, y1=radius, z1=int(z), x2=-2 * radius, y2=0, z2=0, speed=speed)
            tello.curve_xyz_speed(x1=radius, y1=-radius, z1=int(-z), x2=2 * radius, y2=0, z2=0, speed=speed)


class KivyCamera(Image):
    isConnect: bool
    filename = StringProperty('video.avi')
    frames_per_second = NumericProperty(30.0)
    video_resolution = StringProperty('720p')
    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    def __init__(self, capture, fps, **kwargs):
        self.dropdown = CustomDropDown()
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.isConnect = True
        self.cap = None
        self.forward = None
        self.backward = None
        self.left = None
        self.Camera = None
        self.Right = None
        self.up = None
        self.down = None
        self.rotateR = None
        self.rotateL = None
        self.flip_thread = None
        self.frame = None
        self.recordingVideo = False
        self.motoronbool = False
        self.FbRange = [6200, 6800]
        self.pid = [0.4, 0.4, 0]
        self.pError = 0
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self.mainButton = Button(text='Menu', size=(150, 50), pos=(650, 550))
        self.add_widget(self.mainButton)
        self.mainButton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        try:
            self.capture.connect()
        except Exception as e:
            if str(e) == "Command 'command' was unsuccessful for 2 tries. Latest response:	'Aborting command " \
                         "'command'. Did not receive a response after 7 seconds'":
                self.isConnect = False
        if self.isConnect is True:
            self.capture.streamon()
            self.ids.not_connected.color = (0, 0, 0, 0)
            Clock.schedule_interval(self.update, 1.0 / fps)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.on_move_forward()
        elif keycode[1] == 'down':
            self.on_move_backward()
        elif keycode[1] == 'left':
            self.on_move_left()
        elif keycode[1] == 'right':
            self.on_move_right()
        elif keycode[1] == 'z':
            self.on_move_up()
        elif keycode[1] == 's':
            self.on_move_down()
        elif keycode[1] == 'q':
            self.on_move_rotateL()
        elif keycode[1] == 'd':
            self.on_move_rotateR()
        elif keycode[1] == 'a':
            self.takeoff()
        elif keycode[1] == 'e':
            self.land()
        elif keycode[1] == 'p':
            self.on_capture_image()
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'up':
            self.off_move_forward()
        elif keycode[1] == 'down':
            self.off_move_backward()
        elif keycode[1] == 'left':
            self.off_move_left()
        elif keycode[1] == 'right':
            self.off_move_right()
        elif keycode[1] == 'z':
            self.off_move_up()
        elif keycode[1] == 's':
            self.off_move_down()
        elif keycode[1] == 'q':
            self.off_move_rotateL()
        elif keycode[1] == 'd':
            self.off_move_rotateR()
        elif keycode[1] == 'p':
            self.on_capture_image()
        return True

    def update(self, dt):
        self.frame = self.capture.get_frame_read().frame
        if self.dropdown.isFaceTracking and self.capture.get_flight_time != 0 and self.capture.get_height != 0:
            h = threading.Thread(name='FaceTracking', target=self.Start_up(self.frame, self.capture))
            h.start()
        if self.dropdown.isQrCodeAction:
            self.detectQrCode(self.frame)
        if self.dropdown.isRoundMod and self.capture.get_flight_time != 0 and self.capture.get_height != 0:
            h = threading.Thread(name='360', target=self.round)
            h.start()
            self.dropdown.isRoundMod = False
        if self.dropdown.isReboundMod and self.capture.get_flight_time != 0 and self.capture.get_height != 0:
            h = threading.Thread(name='rebound', target=self.rebound)
            h.start()
            self.dropdown.isReboundMod = False
        if self.dropdown.isBigAngle and self.capture.get_flight_time != 0 and self.capture.get_height != 0:
            h = threading.Thread(name='BigAngle', target=self.bigAngle)
            h.start()
            self.dropdown.isBigAngle = False
        buf1 = cv2.flip(self.frame, 0)
        buf = buf1.tobytes()
        image_texture = Texture.create(size=(self.frame.shape[1], self.frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.texture = image_texture
        self.ids.battery_label.text = "Battery: " + str(self.capture.get_battery()) + "%"
        self.ids.temperature_label.text = "Temperature: " + str(self.capture.get_temperature()) + "°C"
        self.ids.barometer_label.text = "Altitude: " + str(self.capture.get_height()) + "cm"
        self.ids.time_flight_label.text = "Flight Time: " + str(self.capture.get_flight_time()) + "s"
        if self.dropdown.isFaceTracking is not True and self.capture.get_height() != 0:
            self.capture.send_rc_control(0, 0, 0, 0)

    def bigAngle(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            ts = datetime.datetime.now()
            filename = "{}.avi".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
            p = Path(__file__).parent
            p = PurePath(p, 'Resources', 'Videos', filename)
            p = str(p)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_writer = cv2.VideoWriter(p, fourcc, 45, (960, 720))
            max_height = self.capture.get_height() + 50
            while max_height >= self.capture.get_height():
                self.capture.send_rc_control(0, -50, 50, 0)
                video_writer.write(self.capture.get_frame_read().frame)

    def rebound(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            while self.capture.get_height() > 50:
                self.capture.send_rc_control(0, 0, -50, 0)
            while self.capture.get_height() < 120:
                self.capture.send_rc_control(0, 0, 50, 0)
            while self.capture.get_height() > 80:
                self.capture.send_rc_control(0, 0, -50, 0)

    def round(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            self.capture.rotate_clockwise(360)

    def doCircle(self, direction, radius, inclinaison):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            h = threading.Thread(name='circle', target=circle(radius, direction, "cw", inclinaison, 50, self.capture))
            h.start()

    def detectQrCode(self, img):
        det = decode(img)

        for barcode in det:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            tmp = barcodeData.split()
            print(tmp)
            if barcodeData == "facetracking":
                self.dropdown.isFaceTracking = True
            elif barcodeData == "QrcodeAction":
                self.dropdown.isQrCodeAction = not self.dropdown.isQrCodeAction
            elif barcodeData == "bigAngle":
                self.dropdown.isBigAngle = True
            elif barcodeData == "360Mod":
                self.dropdown.isRoundMod = True
            elif barcodeData == "Rebound":
                self.dropdown.isReboundMod = True
            elif tmp[0] == "circle":
                h = threading.Thread(name='circle',
                                     target=circle(int(tmp[1]), tmp[2], tmp[3], int(tmp[4]), 50, self.capture))
                h.start()
            elif barcodeData is not None:
                h = threading.Thread(name='qrcode', target=self.capture.send_command_with_return(barcodeData))
                h.start()
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    def flip(self, direction):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.flip_thread is not None:
                self.flip_thread.stop = False
                self.flip_thread = None
            self.flip_thread = threading.Thread(name='flip', target=self.threadFlip(direction))
            self.flip_thread.start()

    def threadFlip(self, direction):
        if direction == "l":
            self.capture.flip_left()
        elif direction == "r":
            self.capture.flip_right()
        elif direction == "f":
            self.capture.flip_forward()
        elif direction == "b":
            self.capture.flip_backwad()
        else:
            pass

    def Start_up(self, cap, me):
        detector = FaceTracking.FaceDetector()
        img = detector.findFaces(cap, me)

        return img

    def on_capture_image(self):
        self.takePicture('%s.png' % timestamp())

    def off_capture_image(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.capture is not None:
                self.capture.stop = False
                self.capture = None

    def on_Video_recorder(self):
        self.startOrStopVideo('%s.avi' % timestamp())

    def off_Video_recorder(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.capture is not None:
                self.capture.stop = False
                self.capture = None


    # Move Forward
    def on_move_forward(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.forward is not None:
                self.forward.stop = False
                self.forward = None
            self.forward = threading.Thread(name='move_forward', target=self.move_forward)
            self.forward.start()

    def move_forward(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 50, 0, 0)

    def off_move_forward(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.forward is not None:
                self.forward.stop = False
                self.forward = None

    # Move Backward
    def on_move_backward(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.backward is not None:
                self.backward.stop = False
                self.backward = None
            self.backward = threading.Thread(name='move_backward', target=self.move_backward)
            self.backward.start()

    def move_backward(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, -50, 0, 0)

    def off_move_backward(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.backward is not None:
                self.backward.stop = False
                self.backward = None

    # Move Right
    def on_move_right(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.Right is not None:
                self.Right.stop = False
                self.Right = None
            self.Right = threading.Thread(name='move_right', target=self.move_right)
            self.Right.start()

    def takePicture(self, fileName):
        ''' take a picture and save to a png file '''
        timePrint('Taking picture to %s' %fileName)
        frame_read = self.frame
        cv2.imwrite(fileName, frame_read)
        timePrint('Saved picture to %s' %fileName)

    def startOrStopVideo(self, fileName):
        if not self.recordingVideo:
            self.startVideo(fileName)
        else:
            self.stopVideo()

    def startVideo(self, fileName):
        ''' start a video and save to a avi file '''
        self.recordingVideo = True
        self.recorder = startThread(context='Video Recording to %s' %fileName, target=self._videoRecorder, front=True, args=(fileName,))

    def stopVideo(self):
        if self.recordingVideo:
            self.recordingVideo = False
            self.recorder.join()

    def _videoRecorder(self, fileName):
        # create a VideoWrite object, recoring to avi file
        frame_read = self.frame
        height, width, _ = frame_read.shape
        timePrint('Starting video recording (%ix%i) to file %s' %(width, height, fileName))
        video = cv2.VideoWriter(fileName, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))

        while self.recordingVideo:
            video.write(frame_read)
            time.sleep(1 / 30)

        video.release()
        timePrint('Stopped video recording')

    def move_right(self):
        t = threading.currentThread()

        while getattr(t, "stop", True):
            self.capture.send_rc_control(50, 0, 0, 0)

    def off_move_right(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.Right is not None:
                self.Right.stop = False
                self.Right = None

    # Move left
    def on_move_left(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.left is not None:
                self.left.stop = False
                self.left = None
            self.left = threading.Thread(name='move_left', target=self.move_left)
            self.left.start()

    def move_left(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(-50, 0, 0, 0)

    def off_move_left(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.left is not None:
                self.left.stop = False
                self.left = None

    # Move Up
    def on_move_up(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.up is not None:
                self.up.stop = False
                self.up = None
            self.up = threading.Thread(name='move_up', target=self.move_up)
            self.up.start()

    def move_up(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 0, 50, 0)

    def off_move_up(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.up is not None:
                self.up.stop = False
                self.up = None

    # Move Down
    def on_move_down(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.down is not None:
                self.down.stop = False
                self.down = None
            self.down = threading.Thread(name='move_down', target=self.move_down)
            self.down.start()

    def move_down(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 0, -50, 0)

    def off_move_down(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.down is not None:
                self.down.stop = False
                self.down = None

    # Rotate Right
    def on_move_rotateR(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.rotateR is not None:
                self.rotateR.stop = False
                self.rotateR = None
            self.rotateR = threading.Thread(name='move_rotateR', target=self.move_rotateR)
            self.rotateR.start()

    def move_rotateR(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 0, 0, 50)

    def off_move_rotateR(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.rotateR is not None:
                self.rotateR.stop = False
                self.rotateR = None

    # Rotate Left
    def on_move_rotateL(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.rotateL is not None:
                self.rotateL.stop = False
                self.rotateL = None
            self.rotateL = threading.Thread(name='move_rotateL', target=self.move_rotateL)
            self.rotateL.start()

    def move_rotateL(self):
        t = threading.currentThread()
        while getattr(t, "stop", True):
            self.capture.send_rc_control(0, 0, 0, -50)

    def off_move_rotateL(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            if self.rotateL is not None:
                self.rotateL.stop = False
                self.rotateL = None

    def takeoff(self):
        if self.capture.stream_on is False or self.capture.get_height() != 0:
            pass
        else:
            h = threading.Thread(name='takeoff', target=self.takeoffThread)
            h.start()

    def takeoffThread(self):
        self.capture.takeoff()

    def throwfly(self):
        if self.capture.stream_on is False or self.capture.get_height() != 0:
            pass
        else:
            h = threading.Thread(name='throwfly', target=self.throwflyThread)
            h.start()

    def throwflyThread(self):
        self.capture.send_command_with_return("throwfly")

    def motoron(self):
        if self.capture.stream_on is False or self.capture.get_height() != 0:
            pass
        else:
            if self.motoronbool is False:
                h = threading.Thread(name='motoron', target=self.motoronThread)
                h.start()
                self.motoronbool = True
            elif self.motoronbool is True:
                h = threading.Thread(name='motoroff', target=self.motoroffThread)
                h.start()
                self.motoronbool = False

    def motoroffThread(self):
        self.capture.send_command_with_return("motoroff")

    def motoronThread(self):
        self.capture.send_command_with_return("motoron")

    def land(self):
        if self.capture.stream_on is False or self.capture.get_flight_time() == 0 and self.capture.get_height() == 0:
            pass
        else:
            h = threading.Thread(name='land', target=self.landThread)
            h.start()

    def landThread(self):
        self.capture.land()


class TelloApp(App):

    def __init__(self, tel, **kwargs):
        super(TelloApp, self).__init__(**kwargs)
        self.me = tel

    def build(self):
        my_camera = KivyCamera(capture=self.me, fps=30)
        return my_camera

    def on_stop(self):
        if self.me.stream_on is True:
            self.me.streamoff()
            self.me.send_command_with_return("motoroff")
            if self.me.get_height() != 0:
                self.me.land()

if __name__ == '__main__':
    tell = tello.Tello(retry_count=1)
    TelloApp(tell).run()
