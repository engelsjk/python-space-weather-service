"""
__init__.py
Flask app initialization with configuration loading and monitor scheduling.
"""

from flask import Flask
import os
import json
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)

from app import views
from app import processes

##############################################
# DEFINE SETTINGS

config_file = 'config.json'

##############################################
# DEFINE FUNCTIONS

def start_monitor():
    """Define and start scheduled monitoring service."""
    monitor_enabled = config_json[env]['MONITOR_ENABLED']
    monitor_trigger_interval_s = int( config_json[env]['MONITOR_TRIGGER_INTERVAL_S'] )

    # IF SCHEDULE IS ENABLED IN CONFIG:
    if monitor_enabled == "1":

        print("\nSpace Weather Service Monitor: ENABLED (running every %s seconds)" % monitor_trigger_interval_s)

        # RUN INITIAL CHECK SPACE WEATHER
        processes.process_check_space_weather()

        # CREATE SCHEDULER W/ INTERVAL TRIGGER AND START
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func = processes.process_check_space_weather,
            trigger = IntervalTrigger( seconds = monitor_trigger_interval_s ),
            id = 'check_space_weather',
            name = 'Checking Space Weather Every 30 Seconds')
        scheduler.start()
        atexit.register( lambda: scheduler.shutdown() )
    else:
        print("\nSpace Weather Service Monitor: DISABLED")

##############################################
##############################################
# RESET STATE (LOCAL FILE)

processes.reset_state()

##############################################
# LOAD CONFIGURATION FILE AND UPDATE APP CONFIG

with open( config_file ) as config_json_file:
    config_json = json.load( config_json_file )
env = os.getenv( 'FLASK_ENV' )

if env not in config_json:
    print("\nPlease check your FLASK_ENV setting and make sure it matches up with an environment definition in config.json!")
else:
    app.config.update( config_json[env] )
    start_monitor()




