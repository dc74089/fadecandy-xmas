from flask import Flask, request, redirect
from flask.templating import render_template

from lightcontrol import LightController

app = Flask(__name__)
lc = LightController()
animations = {}
statics = {}

animations[0] = "All Off"
animations[1] = "Red/Green Fade"
animations[2] = "Red/Green Wipe"
animations[3] = "White Twinkle"
animations[4] = "Christmas Twinkle"

statics[100] = "Red/Green"
statics[101] = "White"


@app.route('/')
def index():
    return render_template("lightactivation.html", alist = animations, slist = statics)


@app.route('/setstate/:newstate')
def set_state(newstate = 0):
    set_state_if_int(newstate)
    return redirect('/')


@app.route('/setstate')
def set_state_from_args():
    set_state_if_int(request.args['routine'])
    return redirect('/')


def set_state_if_int(newstate):
    try:
        state_to_set = int(newstate)
        lc.setstate(state_to_set)
        print "New state: %i" % state_to_set
    except ValueError:
        print "Not an int"


if __name__ == '__main__':
    app.debug = False
    app.run(port = 1150)
