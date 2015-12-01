import threading
import opc
import random
import time

GRG_LEN = 150
PERIOD = 1024

j = lambda: int(round(time.time() * 1000)) % PERIOD
time = lambda: int(round(time.time() * 1000))


class GarageController(threading.Thread):
    def __init__(self, ip='127.0.0.1:7890'):
        threading.Thread.__init__(self)
        
        self.fc = opc.Client(ip)
        self.state = 0
        self.pixels = []

        # Test if it can connect (optional)
        if self.fc.can_connect():
            print('Connected')
        else:
            print('WARNING: could not connect')

    def setstate(self, state):
        self.state = state

    def run(self):
        while(True):
            #TODO: This
            pass

    def fade(self):
        self.pixels = []
        for i in range(GRG_LEN / 2):
            sin = 255 * (0.5 * math.sin(float(j) * 360.0 / float(PERIOD)))
            sin2 = 255 * (0.5 * math.sin(math.pi + (float(j) * 360.0 / float(PERIOD))))

            self.pixels.append((sin, sin2, 0))
            self.pixels.append((sin2, sin, 0))

        self.fc.put_pixels(self.pixels)

    def wipe(self):
        self.pixels = []
        k = time % (GRG_LEN * 2)
        for i in range(GRG_LEN):
            if k < GRG_LEN:
                if i < k:
                    self.pixels.append((255, 0, 0))
                else:
                    self.pixels.append((0, 255, 0))
            else:
                if (GRG_LRN + i) < k:
                    self.pixels.append((0, 255, 0))
                else:
                    self.pixels.append((255, 0, 0))
        self.fc.put_pixels(self.pixels)

    def twinkle(self):
        self.pixels = []
        for i in range(GRG_LEN):
            if(randint(0, 10000) < 20):
                self.pixels.append((255, 255, 175))
            else:
                self.pixels.append((128, 140, 65))



                
