from bottle import route, run, template
import traceback
from lightcontrol import LightController

lc = LightController()

@route('/opc/setstate/:newstate')
def setState(newstate = 0):
    setstateifint(newstate)
    return newstate

@route('/opc/getstates')
def listStates():
    return '''
{
    0 : "All Off",
    1 : "Red/Green Fade",
    2 : "Red/Green Wipe",
    3 : "White Twinkle",
    4 : "Red/Green/White Twinkle",
    5 : "Christmas Cylon",
    100 : "Static Red/Green",
    101 : "White Static"
}
    '''

def setstateifint(newstate):
    try:
        statetoset = int(newstate)
        lc.setstate(statetoset)
        print "New state: %i" % statetoset
    except ValueError:
        print "Not an int"
    
lc.start()
run(host='0.0.0.0', port=1150)
