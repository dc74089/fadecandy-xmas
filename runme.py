import os

from flask import Flask, request, redirect
from flask.templating import render_template

from garage import GarageController

app = Flask(__name__)

gc = GarageController()
gc.daemon = True
gc.start()

animations = {}
statics = {}

animations[0] = "All Off"
animations[1] = "Red/Green Fade"
animations[2] = "Red/Green Wipe"
animations[3] = "White Twinkle"
animations[4] = "Christmas Twinkle"
animations[901] = "Hurricane Monitor"
#animations[13] = "Halloween" #App Only
#animations[14] = "Scare" #App Only
#animations[5] = "Cylon" #UGLY

statics[100] = "Red/Green"
statics[101] = "White"
statics[999] = "Special Day (must be preset)"

print "Runme: I am %i" % os.getpid()


@app.route('/')
def index():
    return render_template("lightactivation.html", alist=animations, slist=statics, title="Canora Lights",
                           special=gc.is_special_day)


@app.route('/test')
def test():
    return "Hello World!"


@app.route('/admin', methods=['GET'])
def admin_serve():
    return render_template("admin.html", title="Admin")


@app.route('/setstate', methods=['POST'])
def set_state_from_args():
    set_state_if_int(request.form['routine'])
    return redirect("/")


@app.route('/testshow')
def test_show():
    gc.test_show()
    return "Starting show..."


@app.route('/enabledebug')
def enable_debug():
    gc.debug = True
    return "Debug Enabled"


@app.route('/disabledebug')
def disable_debug():
    gc.debug = False
    return "Debug Disabled"


#@app.route('/shutdown')
def shutdown():
    shutdown_server()
    os.system('kill %d' % os.getpid())
    return "Shutting down..."


#def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def set_state_if_int(newstate):
    try:
        state_to_set = int(newstate)
        gc.setstate(state_to_set)
        print "New state: %i" % state_to_set
    except ValueError:
        print "Not an int"


if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0", port=1150)
