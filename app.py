from flask import Flask, render_template
# from flask_bcrypt import Bcrypt
from logging import FileHandler, Formatter
import datetime
# from urllib.parse import urlsplit
# import pymongo
import os
import time
import pyowm


# initialization #
# create instance of Flask class
app = Flask(__name__)
# bcrypt = Bcrypt(app)
app.config.update(SECRET_KEY='what_a_big_secret')

# open weather map api
OWM_API_KEY = '9e4c3c5c1830e887ac0d71df220e9cbe'
owm = pyowm.OWM(OWM_API_KEY)

# define error logging #
basedir = os.path.abspath(os.path.dirname(__file__))
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter('[%(asctime]s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
)
app.logger.addHandler(handler)

# mongo database setup #
# mongo_url = os.getenv('MONGOLAB_URI', 'mongodb://heroku_h647qr53:ckmlb3pfoqtmfqp3irv94maipl@ds145415.mlab.com:45415/heroku_h647qr53')
# if mongo_url:
#     parsed = urlsplit(mongo_url)
#     db_name = parsed.path[1:]
#     db = pymongo.MongoClient(mongo_url)[db_name]
#     # users = db['users']
# else:
#     conn = pymongo.MongoClient()
#     db = conn['db']
#     # users = db['users']


# GET TIMING THINGS #
def get_current_time():
    return time.ctime().split(' ')[4][:-3]


def get_dow():
    return time.ctime().split(' ')[0]


def get_month():
    return str(time.ctime().split(' ')[1])


def get_date():
    return str(time.ctime().split(' ')[3])


# get current weather and forcasted weather
observation = owm.weather_at_place('Evanston, IL')
w = observation.get_weather()

# forecast = owm.daily_forecast("Milan,it")
# tomorrow = pyowm.timeutils.tomorrow()


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


# assign weather icon
def assign_icon():
    cloud_perc = w.get_clouds()
    # utc minus 5, server is on utc
    start = datetime.time(17, 0, 0)
    end = datetime.time(7, 0, 0)
    night = time_in_range(start, end, datetime.datetime.now().time())
    if len(w.get_snow().items()) != 0:
        return "fa fa-snowflake-o"
    elif len(w.get_rain().items()) != 0:
        return "fa fa-umbrella"
    elif cloud_perc < 50 and night is True:
        return "fa fa-moon-o"
    elif cloud_perc < 50 and night is False:
        return "fa fa-sun-o"
    else:
        return "fa fa-cloud"


# template routes #
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html',
                           time=get_current_time(),
                           dow=get_dow(),
                           month=get_month(),
                           date=get_date(),
                           temp=w.get_temperature('fahrenheit'),
                           humidity=w.get_humidity(),
                           icon=assign_icon()
                           )


# the weather api is limited in the number of daily requests, so we need to retrieve that info every hour
# and store it temporarily
# then figure out a way to update the clock every minute


# run #
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
