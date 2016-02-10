import threading
import time
from datetime import datetime
from math import *
from random import randint

import opc

GRG_LEN = 150
PERIOD = 1024
SLEEP = 0.01
HIBERNATE = 60

AUTO_ON_ENABLED_DAILY = False
DAILY_START_PROGRAM = 4

AUTO_ON_ENABLED_SPECIAL = True

START_TIME = lambda: datetime.now().replace(hour=17, minute=30, second=0)
BEDTIME = lambda: datetime.now().replace(hour=23, minute=30, second=0)
now = lambda: datetime.now()

j = lambda: int(round(time.time() * 10)) % PERIOD
theTime = lambda: int(round(time.time() * 10))


class GarageController(threading.Thread):
    def __init__(self, ip='127.0.0.1:7890', debug=False):
        threading.Thread.__init__(self)

        self.fc = opc.Client(ip)
        self.debug = debug
        self.state = 0
        self.direction = True
        self.position = 0
        self.initialized = False
        self.manual_show_test = False
        self.timetillon = datetime.now().time()
        self.timetilloff = datetime.now().time()
        self.specialdays = {}
        self.is_special_day = False
        self.special_day_colors = None
        self.last_initialized_date = datetime.min.date()
        self.initspecialdays()
        self.check_special_day()

        if self.fc.can_connect():
            print('Connected')
        else:
            print('WARNING: could not connect to fadecandy')

    def initspecialdays(self):
        self.specialdays[(2, 14)] = ((255, 116, 140), (255, 0, 0), (255, 255, 175)) #Valentines Day
        self.specialdays[(4, 2)] = ((0, 255, 255), (255, 255, 175)) #Light it up blue
        self.specialdays[(3, 17)] = ((0, 255, 0), (255, 255, 175)) #St. Patrick's
        self.specialdays[(2, 10)] = ((255, 116, 140), (255, 0, 0), (255, 255, 175))  # DEBUG

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
            elif self.state == 999:
                self.special_day_static()
            # Default to off
            else:
                self.all_off()

            time.sleep(SLEEP)

            self.timetillon = START_TIME() - now()
            self.timetilloff = BEDTIME() - now()
            
            if self.last_initialized_date < now().date(): #Check if today is a special day, once per day
                self.check_special_day()
                self.last_initialized_date = now().date()
                
            if self.is_special_day and START_TIME() <= now() <= BEDTIME() and AUTO_ON_ENABLED_SPECIAL \
                    and not self.initialized:
                self.state = 999
                self.initialized = True

            if self.manual_show_test: #Test show manually, if needed
                self.init_show()
                self.manual_show_test = False
                self.state = 0

            if AUTO_ON_ENABLED_DAILY and START_TIME() <= now() <= BEDTIME() and not self.initialized\
                    and not self.is_special_day: #Daily Init
                if self.state == 0:
                    self.init_show()
                    self.state = DAILY_START_PROGRAM
                self.initialized = True

            if now() >= BEDTIME(): #Daily shutoff and un-init, every day
                self.state = 0
                self.initialized = False

            if self.state == 0 and not self.debug:
                self.all_off()
                time.sleep(HIBERNATE)

    def test_show(self):
        self.manual_show_test = True

    def check_special_day(self):
        if any(now().month == tup[0] and now().day == tup[1] for tup in self.specialdays.keys()):
            self.is_special_day = True
            self.special_day_colors = self.specialdays.get((now().month, now().day), (0, 0, 0))
        else:
            self.is_special_day = False
            self.special_day_colors = None

        if self.debug:
            print ("Special day?: " + str(self.is_special_day))
            print ("Special colors: " + str(self.special_day_colors))

    def init_show(self):
        RAND_DENSITY = 15
        MAX_LOOPS = 10
        SLEEP = 0.75

        self.all_off()
        time.sleep(SLEEP)
        self.fc.put_pixels([])
        time.sleep(SLEEP)
        
        show_colors = []
        for i in range(int(ceil(GRG_LEN / 6))):
            show_colors.append((255, 0, 0))
            show_colors.append((255, 255, 0))
            show_colors.append((0, 255, 0))
            show_colors.append((0, 255, 255))
            show_colors.append((0, 0, 255))
            show_colors.append((255, 0, 255))

        is_colored = [False] * GRG_LEN
        pixels = [(0, 0, 0)] * GRG_LEN

        i = 0

        while any(element is False for element in is_colored):
            for p in range(GRG_LEN):
                if randint(0, 100) < RAND_DENSITY or i is MAX_LOOPS:
                    is_colored[p] = True

                if is_colored[p]:
                    pixels[p] = show_colors[p]
                else:
                    pixels[p] = (0, 0, 0)

            self.fc.put_pixels(pixels)
            time.sleep(SLEEP)

            if i >= MAX_LOOPS:
                break
            i += 1

        i = 0
        time.sleep(SLEEP)

        while any(element is True for element in is_colored):
            for p in range(GRG_LEN):
                if randint(0, 100) < RAND_DENSITY or i is MAX_LOOPS:
                    is_colored[p] = False

                if not is_colored[p]:
                    pixels[p] = (128, 140, 65)
                else:
                    pixels[p] = show_colors[p]

            self.fc.put_pixels(pixels)
            time.sleep(SLEEP)

            if i >= MAX_LOOPS:
                break
            i += 1

        time.sleep(SLEEP * 2)
        pixels = [(255, 255, 175)] * GRG_LEN
        self.fc.put_pixels(pixels)
        time.sleep(SLEEP * 3)

        i = 100
        while i > 0:
            for p in range(GRG_LEN):
                if randint(0, 100) < i:
                    pixels[p] = (255, 255, 175)
                else:
                    pixels[p] = (0, 0, 0)
            self.fc.put_pixels(pixels)
            i -= 1
            time.sleep(0.04)

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

    def special_day_static(self):
        try:
            num_colors = len(self.special_day_colors)
        except TypeError:
            return

        pixels = []
        for i in range(GRG_LEN):
            pixels.append(((self.special_day_colors[i % num_colors][1]), (self.special_day_colors[i % num_colors][0]),
                           (self.special_day_colors[i % num_colors][2])))  # Because GRB colors are nasty

        self.fc.put_pixels(pixels)

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
