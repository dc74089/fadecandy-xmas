from flask import Flask, request, redirect
from flask.templating import render_template
from lightcontrol import LightController
from datetime import datetime

app = Flask(__name__)

lc = LightController()
lc.start()

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
    return render_template("lightactivation.html", alist=animations, slist=statics)


@app.route('/test')
def test():
    return "test"


@app.route('/time')
def test_time():
    return "Datetime: %s <br> Hour: %f" % (str(datetime.now()), datetime.now().hour)


@app.route('/suninfo')
def suninfo():
    from astral import Astral
    a = Astral()
    orlando = a['Orlando']
    sun = orlando.sun(date=datetime.now(), local=True)
    return "Dawn: %s<br>Sunrise: %s<br>Noon: %s<br>Sunset: %s<br>Dusk: %s<br>Now: %s<br><br>Time till on %s: <br>" \
           "Time till off: %s" % (
    str(sun['dawn']), str(sun['sunrise']), str(sun['noon']), str(sun['sunset']), str(sun['dusk']),
    str(sun['dusk'].tzinfo.localize(datetime.now())), str(lc.timetillon), str(lc.timetilloff))


@app.route('/setstate', methods=['POST'])
def set_state_from_args():
    set_state_if_int(request.form['routine'])
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
    app.run(host="0.0.0.0", port=1150)
