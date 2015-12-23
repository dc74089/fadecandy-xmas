import threading

from datetime import datetime

import opc
from random import randint
from math import *
import time
from astral import Astral

GRG_LEN = 150
PERIOD = 1024
SLEEP = 0.01
HIBERNATE = 60

AUTO_ON_ENABLED = True
START_PROGRAM = 4
BEDTIME_HOUR = 23
astral = Astral()
orlando = astral["Orlando"]

j = lambda: int(round(time.time() * 10)) % PERIOD
theTime = lambda: int(round(time.time() * 10))


class LightController(threading.Thread):
    def __init__(self, ip='127.0.0.1:7890'):
        threading.Thread.__init__(self)

        self.fc = opc.Client(ip)
        self.state = 0
        self.direction = True
        self.position = 0
        self.initialized = False
        self.manual_show_test = False
        self.timetillon = datetime.now()
        self.timetilloff = datetime.now()

        self.colors = []
        for i in range(int(ceil(GRG_LEN / 6))):
            self.colors.append((255, 0, 0))
            self.colors.append((255, 255, 0))
            self.colors.append((0, 255, 0))
            self.colors.append((0, 255, 255))
            self.colors.append((0, 0, 255))
            self.colors.append((255, 0, 255))

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
        print 'State set to %f' % state

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
            # Default to off
            else:
                self.all_off()

            time.sleep(SLEEP)

            now = datetime.now()

            sun = orlando.sun(date=now, local=True)
            sunset = sun['sunset']

            now = sunset.tzinfo.localize(now)

            bedtime = sunset.replace(hour=BEDTIME_HOUR, minute=0, second=0)

            self.timetillon = sunset - now
            self.timetilloff = bedtime - now

            if self.manual_show_test:
                self.all_off()
                time.sleep(1)
                self.init_show()
                self.manual_show_test = False

            if sunset <= now <= bedtime and not self.initialized:
                if self.state == 0:
                    #self.init_show()
                    self.state = START_PROGRAM
                self.initialized = True

            if now >= bedtime:
                self.state = 0
                self.initialized = False
                time.sleep(HIBERNATE)

    def test_show(self):
        self.manual_show_test = True

    def init_show(self):
        self.all_off()

        i = pow(2, 100)
        pixels = [(0, 0, 0)] * GRG_LEN

        while i > 1:
            for p in range(GRG_LEN):
                if randint(0, i) < 2:
                    pixels[p] = (128, 140, 65)
            self.fc.put_pixels(pixels)
            i /= 2
            time.sleep(0.5)

        time.sleep(0.5)
        pixels = [(255, 255, 175)] * GRG_LEN
        self.fc.put_pixels(pixels)

        time.sleep(1)

        active = [True] * GRG_LEN

        i = pow(2, 100)
        while i > 1:
            pixels = [(0, 0, 0)] * GRG_LEN
            for p in range(GRG_LEN):
                if randint(0, i) < 2:
                    active[p] = False

                if randint(0, 10) <= 2 and active[p]:
                    pixels[p] = self.colors[p]
                else:
                    pixels[p] = (0, 0, 0)

            self.fc.put_pixels(pixels)
            i /= 2
            time.sleep(0.5)

        self.all_off()

    def all_off(self):
        pixels = []
        for i in range(GRG_LEN):
            pixels.append((0, 0, 0))
        self.fc.put_pixels(pixels)
        time.sleep(1)

    def fade(self):
        pixels = []
        for i in range(int(ceil(GRG_LEN / 6))):
            sinval = 255 * (0.5 * sin(j() * 180.0 / PERIOD))
            sinval2 = 255 * (0.5 * sin(pi + (j() * 180.0 / PERIOD)))

            pixels.append((sinval, sinval2, 0))
            pixels.append((sinval, sinval2, 0))
            pixels.append((0, 0, 0))
            pixels.append((sinval2, sinval, 0))
            pixels.append((sinval2, sinval, 0))
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
        for i in range(int(ceil(GRG_LEN / 6))):
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
        for i in range(int(ceil(GRG_LEN / 6))):
            pixels.append((255, 0, 0))
            pixels.append((255, 0, 0))

            pixels.append((0, 0, 0))

            pixels.append((0, 255, 0))
            pixels.append((0, 255, 0))

            pixels.append((0, 0, 0))
        self.fc.put_pixels(pixels)

    def white_static(self):
        pixels = []
        for i in range(GRG_LEN):
            pixels.append((255, 255, 175))
        self.fc.put_pixels(pixels)
