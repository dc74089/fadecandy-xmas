from bottle import route, run, template
import traceback
from lightcontrol import *

gc = GarageController()

@route('/opc/setstate/:newstate')
def setState(newstate = 0):
    setstateifint(newstate)
    return newstate

@route('/opc/getstates')
def printStates():
    return """
        {
            "Red/Green Fade": 1,
            "Red/Green Wipe": 2,
            "White Twinkle": 3
        }
    """

def setstateifint(newstate):
    try:
        statetoset = int(newstate)
        gc.setstate(statetoset)
        print "New state: %i" % statetoset
    except ValueError:
        print "Not an int"
    
gc.start()
run(host='0.0.0.0', port=1150)
