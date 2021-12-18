from kivy import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
from kivy.app import App
from kivy.uix.widget import Widget
import qrcode


class Event(Widget):
    def setChangeText(self, text, explain):
        self.ids.changeText.text = str(text)
        self.ids.explainText.text = str(explain)
        self.ids.error.text = ""
        self.ids.inputText.text = ""

    def generate(self):
        if self.ids.changeText.text == "Move Up":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter a distance in cm between 20 and 500"
            elif self.ids.inputText.text.isdecimal() is False or 20 > int(self.ids.inputText.text) or int(self.ids.inputText.text) > 500:
                self.ids.error.text = "Please enter only number between 20 and 500"
            else:
                img = qrcode.make('up ' + self.ids.inputText.text)
                img.save("QRCodeImg/up-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/up-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Move Down":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter a distance in cm between 20 and 500"
            elif self.ids.inputText.text.isdecimal() is False or 20 > int(self.ids.inputText.text) or int(self.ids.inputText.text) > 500:
                self.ids.error.text = "Please enter only number between 20 and 500"
            else:
                img = qrcode.make('down ' + self.ids.inputText.text)
                img.save("QRCodeImg/down-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/down-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Move Left":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter a distance in cm between 20 and 500"
            elif self.ids.inputText.text.isdecimal() is False or 20 > int(self.ids.inputText.text) or int(self.ids.inputText.text) > 500:
                self.ids.error.text = "Please enter only number between 20 and 500"
            else:
                img = qrcode.make('left ' + self.ids.inputText.text)
                img.save("QRCodeImg/left-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/left-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Move Right":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter a distance in cm between 20 and 500"
            elif self.ids.inputText.text.isdecimal() is False or 20 > int(self.ids.inputText.text) or int(self.ids.inputText.text) > 500:
                self.ids.error.text = "Please enter only number between 20 and 500"
            else:
                img = qrcode.make('right ' + self.ids.inputText.text)
                img.save("QRCodeImg/right-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/right-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Move Forward":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter a distance in cm between 20 and 500"
            elif self.ids.inputText.text.isdecimal() is False or 20 > int(self.ids.inputText.text) or int(self.ids.inputText.text) > 500:
                self.ids.error.text = "Please enter only number between 20 and 500"
            else:
                img = qrcode.make('forward ' + self.ids.inputText.text)
                img.save("QRCodeImg/forward-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/forward-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Move Backward":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter a distance in cm between 20 and 500"
            elif self.ids.inputText.text.isdecimal() is False or 20 > int(self.ids.inputText.text) or int(self.ids.inputText.text) > 500:
                self.ids.error.text = "Please enter only number between 20 and 500"
            else:
                img = qrcode.make('back ' + self.ids.inputText.text)
                img.save("QRCodeImg/backward-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/backward-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Rotate Clockwise":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter a degree"
            elif self.ids.inputText.text.isdecimal() is False:
                self.ids.error.text = "Please enter only number"
            elif int(self.ids.inputText.text) > 360:
                self.ids.error.text = "Please enter only degree between 0 and 360"
            else:
                img = qrcode.make('cw ' + self.ids.inputText.text)
                img.save("QRCodeImg/clockwise-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/clockwise-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Rotate Counter Clockwise" and self.ids.inputText.text != "" and self.ids.inputText.text.isdecimal() is True:
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter a degree"
            elif self.ids.inputText.text.isdecimal() is False:
                self.ids.error.text = "Please enter only number"
            elif int(self.ids.inputText.text) > 360:
                self.ids.error.text = "Please enter only degree between 0 and 360"
            else:
                img = qrcode.make('ccw ' + self.ids.inputText.text)
                img.save("QRCodeImg/counter_clockwise-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/counter_clockwise-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Land":
            if self.ids.inputText.text != "":
                self.ids.error.text = "Please do not write in the text field"
            else:
                img = qrcode.make('land')
                img.save("QRCodeImg/land.png")
                self.ids.qrImage.source = "QRCodeImg/land.png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "TakeOff":
            if self.ids.inputText.text != "":
                self.ids.error.text = "Please do not write in the text field"
            else:
                img = qrcode.make('takeoff')
                img.save("QRCodeImg/takeoff.png")
                self.ids.qrImage.source = "QRCodeImg/takeoff.png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Flip":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please enter the direction of flip in the text field"
            elif self.ids.inputText.text.isdecimal() is True:
                self.ids.error.text = "Please enter only direction indicator"
            elif len(self.ids.inputText.text) != 1 or self.ids.inputText.text != "l" and self.ids.inputText.text != "r" and self.ids.inputText.text != "f" and self.ids.inputText.text != "b":
                self.ids.error.text = "Please enter only direction indicator"
            else:
                img = qrcode.make('flip ' + self.ids.inputText.text)
                img.save("QRCodeImg/flip-" + self.ids.inputText.text + ".png")
                self.ids.qrImage.source = "QRCodeImg/flip-" + self.ids.inputText.text + ".png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "FaceTracking":
            if self.ids.inputText.text != "":
                self.ids.error.text = "Please do not write in the text field"
            else:
                img = qrcode.make('facetracking')
                img.save("QRCodeImg/facetracking.png")
                self.ids.qrImage.source = "QRCodeImg/facetracking.png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "QRcode Tracking":
            if self.ids.inputText.text != "":
                self.ids.error.text = "Please do not write in the text field"
            else:
                img = qrcode.make('QrcodeTracking')
                img.save("QRCodeImg/qrcodetracking.png")
                self.ids.qrImage.source = "QRCodeImg/qrcodetracking.png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "QRCode Action":
            if self.ids.inputText.text != "":
                self.ids.error.text = "Please do not write in the text field"
            else:
                img = qrcode.make('QrcodeAction')
                img.save("QRCodeImg/qrcodeaction.png")
                self.ids.qrImage.source = "QRCodeImg/qrcodeaction.png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "360 Mod":
            if self.ids.inputText.text != "":
                self.ids.error.text = "Please do not write in the text field"
            else:
                img = qrcode.make('360Mod')
                img.save("QRCodeImg/360Mod.png")
                self.ids.qrImage.source = "QRCodeImg/360Mod.png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Rebound Mod":
            if self.ids.inputText.text != "":
                self.ids.error.text = "Please do not write in the text field"
            else:
                img = qrcode.make('Rebound')
                img.save("QRCodeImg/rebound.png")
                self.ids.qrImage.source = "QRCodeImg/rebound.png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "big Angle" and self.ids.inputText.text == "":
            if self.ids.inputText.text != "":
                self.ids.error.text = "Please do not write in the text field"
            else:
                img = qrcode.make('bigAngle')
                img.save("QRCodeImg/bigangle.png")
                self.ids.qrImage.source = "QRCodeImg/bigangle.png"
                self.ids.error.text = ""
        elif self.ids.changeText.text == "Circle Mod":
            if self.ids.inputText.text == "":
                self.ids.error.text = "Please write radius, direction, rotation and inclination"
            tmp = self.ids.inputText.text.split()
            if tmp[0].isdecimal() is False and int(tmp[0]) < 49:
                self.ids.error.text = "Please enter only number for radius and greater or equal than 50"
            elif tmp[2] != "cw" and tmp[2] != "ccw":
                self.ids.error.text = "Please enter only 'cw' or 'ccw' for rotation"
            elif -91 > int(tmp[3]) or int(tmp[3]) > 91:
                self.ids.error.text = "Please enter only number for tilt between -90 and 90"
            elif tmp[1] == "avant" or tmp[1] == "arriere":
                img = qrcode.make('circle ' + tmp[0] + " " + tmp[1] + " " + tmp[2] + " " + tmp[3])
                img.save("QRCodeImg/circle-" + tmp[0] + "-" + tmp[1] + "-" + tmp[2] + "-" + tmp[3] + ".png")
                self.ids.qrImage.source = "QRCodeImg/circle-" + tmp[0] + "-" + tmp[1] + "-" + tmp[2] + "-" + tmp[3] + ".png"
                self.ids.error.text = ""
            else:
                self.ids.error.text = "Please enter only 'avant' or 'arriere' for direction"


class QRCodeApp(App):
    def build(self):
        my_event = Event()
        return my_event


if __name__ == '__main__':
    QRCodeApp().run()
