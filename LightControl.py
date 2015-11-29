import threading
import opc
import random
import time

GRG_LEN = 150
PERIOD = 1024

pixels = []

j = lambda: int(round(time.time() * 1000)) % PERIOD
time = lambda: int(round(time.time() * 1000))


class LightController(threading.Thread):
    def __init__(self, ip='127.0.0.1:7890'):
        threading.Thread.__init__(self)
        
        self.fc = opc.Client(ip)
        self.state = 0

        # Test if it can connect (optional)
        if self.fc.can_connect():
            # Test if it can connect (optional)
            print('Connected')
        else:
            # We could exit here, but instead let's just print a warning
            # and then keep trying to send pixels in case the server
            # appears later
            print('WARNING: could not connect')

    def setstate(state):
        self.state = state

    def run(self):
        while(True):
            print self.state

    def fade(self):
        pixels = []
        for i in range(GRG_LEN / 2):
            sin = 255 * (0.5 * math.sin(float(j) * 360.0 / float(PERIOD)))
            sin2 = 255 * (0.5 * math.sin(math.pi + (float(j) * 360.0 / float(PERIOD))))

            pixels.append((sin, sin2, 0))
            pixels.append((sin2, sin, 0))

        self.fc.put_pixels(pixels)

    def wipe(self):
        pixels = []
        k = time % (GRG_LEN * 2)
        for i in range(GRG_LEN):
            if k < GRG_LEN:
                if i < k:
                    pixels.append((255, 0, 0))
                else:
                    pixels.append((0, 255, 0))
            else:
                if (GRG_LRN + i) < k:
                    pixels.append((0, 255, 0))
                else:
                    pixels.append((255, 0, 0))
        self.fc.put_pixels(pixels)

    def twinkle(self):
        pixels = []
        for i in range(GRG_LEN):
            if(randint(0, 10000) < 20):
                pixels.append((255, 255, 175))
            else:
                pixels.append((128, 140, 65))



                
