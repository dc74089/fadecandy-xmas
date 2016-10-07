import urllib2
import json
import time
import threading

class Weather(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        self.wind = 0
        self.gusts = 0
        self.precip_hour = 0
        self.precip_day = 0

    def run(self):
        try:
            resp = urllib2.urlopen("http://api.wunderground.com/api/3c63d81cbea24dcb/conditions/q/pws:KFLWINTE51.json")
            body = resp.read()
        except URLError:
            pass
        else:
            try:
                data = json.loads(body)
                self.wind = data["current_observation"]["wind_mph"]
                self.gusts = data["current_observation"]["wind_gust_mph"]
                self.precip_hour = data["current_observation"]["precip_1hr_in"]
                self.precip_day = data["current_observation"]["precip_today_in"]

                print "Got wind %d" % self.wind
            except Exception:
                pass

        time.sleep(60*5)

    def get_wind(self):
        return self.wind

    def get_gusts(self):
        return self.gusts

    def get_precip_hour(self):
        return self.precip_hour

    def get_precip_day(self):
        return self.precip_day
