from bottle import route, run, template
import traceback
from LightControl import LightController

lc = LightController()

@route('/opc/setstate/:newstate')
def setState(newstate = 0):
    setstateifint(newstate)
    return newstate

def setstateifint(newstate):
    try:
        statetopset = int(newstate)
        lc.setstate(statetoset)
        print state
    except ValueError:
        print "Not an int"
    
lc.start()
run(host='0.0.0.0', port=80)
