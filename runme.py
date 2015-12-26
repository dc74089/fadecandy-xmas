import os

from flask import Flask, request, redirect
from flask.templating import render_template
from lightcontrol import LightController
from datetime import datetime

app = Flask(__name__)

lc = LightController()
lc.daemon = True
lc.start()

animations = {}
statics = {}

animations[0] = "All Off"
animations[1] = "Red/Green Fade"
animations[2] = "Red/Green Wipe"
animations[3] = "White Twinkle"
animations[4] = "Christmas Twinkle"
animations[5] = "Cylon"

statics[100] = "Red/Green"
statics[101] = "White"


print "Runme: I am %i" % os.getpid()


@app.route('/')
def index():
    return render_template("lightactivation.html", alist=animations, slist=statics, title="Canora Lights")


@app.route('/test')
def test():
    return "Hello World!"


@app.route('/admin', methods=['GET'])
def admin_serve():
    return render_template("admin.html", title="Admin")


@app.route('/admin', methods=['POST'])
def admin_do():
    print("Got a post!")
    return "Hey! How'd you get here?"


@app.route('/suninfo')
def suninfo():
    from astral import Astral
    a = Astral()
    orlando = a['Orlando']
    sun = orlando.sun(date=datetime.now(), local=True)

    display = {}
    display[0] = "Now: %s" % str(sun['dusk'].tzinfo.localize(datetime.now()))
    display[1] = "Dawn: %s" % str(sun['dawn'])
    display[2] = "Sunrise: %s" % str(sun['sunrise'])
    display[3] = "Noon: %s" % str(sun['noon'])
    display[4] = "Sunset: %s" % str(sun['sunset'])
    display[5] = "Dusk: %s" % str(sun['dusk'])
    display[6] = "Time till on: %s" % str(lc.timetillon)
    display[7] = "Time till off: %s" % str(lc.timetilloff)

    return render_template("prettystring.html", dispdict=display, title="Sun Debug")


@app.route('/setstate', methods=['POST'])
def set_state_from_args():
    set_state_if_int(request.form['routine'])
    return redirect('/')


@app.route('/testshow')
def test_show():
    lc.test_show()
    return "Starting show..."


@app.route('/shutdown')
def shutdown():
    shutdown_server()
    os.system('kill %d' % os.getpid())
    return "Shutting down..."


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def set_state_if_int(newstate):
    try:
        state_to_set = int(newstate)
        lc.setstate(state_to_set)
        print "New state: %i" % state_to_set
    except ValueError:
        print "Not an int"


if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0", port=1150)
