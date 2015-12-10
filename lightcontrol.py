import threading
import opc
from random import randint
from math import *
import time

GRG_LEN = 150
PERIOD = 1024
SLEEP = 0.01

j = lambda: int(round(time.time() * 10)) % PERIOD
theTime = lambda: int(round(time.time() * 10))


class LightController(threading.Thread):
    def __init__(self, ip='192.168.0.123:7890'):
        threading.Thread.__init__(self)

        self.fc = opc.Client(ip)
        self.state = 0
        self.direction = True
        self.position = 0

        # Test if it can connect (optional)
        if self.fc.can_connect():
            # Test if it can connect (optional)
            print('Connected')
        else:
            # We could exit here, but instead let's just print a warning
            # and then keep trying to send pixels in case the server
            # appears later
            print('WARNING: could not connect to fadecandy')

    def setstate(self, state):
        self.state = state

    def run(self):
        while True:
            # Kinetics
            if self.state == 1:
                self.fade()
            elif self.state == 2:
                self.wipe()
            elif self.state == 3:
                self.twinkle()
            elif self.state == 4:
                self.red_green_twinkle()
            elif self.state == 5:
                self.cylon()
                # Statics
            elif self.state == 100:
                self.red_green_static()
            elif self.state == 101:
                self.white_static()
                # Finally
            else:
                self.all_off()

            time.sleep(SLEEP)

    def all_off(self):
        pixels = []
        for i in range(GRG_LEN):
            pixels.append((0, 0, 0))
        self.fc.put_pixels(pixels)

    def fade(self):
        pixels = []
        for i in range(int(math.ceil(GRG_LEN / 6))):
            sin = 255 * (0.5 * math.sin(j() * 180.0 / PERIOD))
            sin2 = 255 * (0.5 * math.sin(math.pi + (j() * 180.0 / PERIOD)))

            pixels.append((sin, sin2, 0))
            pixels.append((sin, sin2, 0))
            pixels.append((0, 0, 0))
            pixels.append((sin2, sin, 0))
            pixels.append((sin2, sin, 0))
            pixels.append((0, 0, 0))

        self.fc.put_pixels(pixels)

    def wipe(self):
        pixels = []
        k = (theTime() % (GRG_LEN * 2))
        for i in range(GRG_LEN):
            if k < GRG_LEN:
                if i < k:
                    pixels.append((255, 0, 0))
                else:
                    pixels.append((0, 255, 0))
            else:
                if (GRG_LEN + i) < k:
                    pixels.append((0, 255, 0))
                else:
                    pixels.append((255, 0, 0))
        self.fc.put_pixels(pixels)

    def twinkle(self):
        pixels = []
        for i in range(GRG_LEN):
            if randint(0, 10000) < 20:
                pixels.append((255, 255, 175))
            else:
                pixels.append((128, 140, 65))
        self.fc.put_pixels(pixels)

        time.sleep(0.04)

    def red_green_twinkle(self):
        pixels = []
        for i in range(int(math.ceil(GRG_LEN / 6))):
            pixels.append((255, 0, 0))
            # pixels.append((255, 0, 0))

            if randint(0, 10000) < 20:
                pixels.append((255, 255, 175))
            else:
                pixels.append((128, 140, 65))

            if randint(0, 10000) < 20:
                pixels.append((255, 255, 175))
            else:
                pixels.append((128, 140, 65))

            pixels.append((0, 255, 0))
            # pixels.append((0, 255, 0))

            if randint(0, 10000) < 20:
                pixels.append((255, 255, 175))
            else:
                pixels.append((128, 140, 65))

            if randint(0, 10000) < 20:
                pixels.append((255, 255, 175))
            else:
                pixels.append((128, 140, 65))

        self.fc.put_pixels(pixels)

    def cylon(self):
        pixels = []
        for i in range(GRG_LEN):
            pixels.append((0, 0, 0))

        try:
            pixels[self.position] = (128, 0, 0)
            pixels[self.position + 1] = (0, 255, 0)
            pixels[self.position + 2] = (128, 0, 0)
        except IndexError:
            self.direction = not self.direction

        self.fc.put_pixels(pixels)

        if self.position <= 1:
            self.direction = True

        if self.direction:
            self.position += 1
        else:
            self.position -= 1

        time.sleep(0.01)

    # Statics

    def red_green_static(self):
        pixels = []
        for i in range(int(math.ceil(GRG_LEN / 6))):
            pixels.append((255, 0, 0))
            pixels.append((255, 0, 0))

            pixels.append((0, 0, 0))

            pixels.append((0, 255, 0))
            pixels.append((0, 255, 0))

            pixels.append((0, 0, 0))
        print 'Putting Pixels'
        self.fc.put_pixels(pixels)

    def white_static(self):
        pixels = []
        for i in range(GRG_LEN):
            pixels.append((255, 255, 175))
        self.fc.put_pixels(pixels)
