"""
views.py
Define app server routes (based on processes.py functions).
"""

from flask import jsonify, render_template
import json

from app import app

from app import processes
from app import errors

##############################################
# APP ROUTES 

@app.route('/')
def index():
    return "Hello, World!"

@app.route( '/check-space-weather' )
def check_space_weather():
    """Returns JSON payload of space weather check output."""
    payload = processes.process_check_space_weather()
    return json.dumps( payload )
        
@app.route( '/get-data' )
def get_data():
    """Returns JSON payload of data output."""
    payload = processes.process_get_data()
    return json.dumps( payload )

@app.route( '/get-data-by-signal/<signal>' )
def get_data_by_signal( signal ):
    """Returns JSON payload of data by signal output."""
    payload = processes.process_get_data_by_signal( signal )
    return json.dumps( payload )

@app.errorhandler( errors.GeneralError )
def handle_general_error( error ):
    """Returns general error response."""
    response = jsonify( error.to_dict() )
    response.status_code = error.status_code
    return response

@app.errorhandler( 404 )
def page_not_found( e ):
    """Returns JSON payload for a basic 404 response."""
    return jsonify( error=404, message='endpoint-does-not-exist' ), 404

###########################################

