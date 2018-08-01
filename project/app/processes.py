"""
processes.py
Define contained processes to be used by either the monitor or API.
"""

from datetime import datetime

from app import app

from app.monitors import SpaceWeatherMonitor
from app.data import SpaceWeatherData
from app.filemanagers import FileManager
from app.actions import ActionHandler
from app.plots import Plotter

##############################################
# RUN CHECK SPACE WEATHER PROCESS


def process_check_space_weather(): 
    """Runs through space weather monitoring logic."""
    
    signal = 'P10'

    # INITILIAZE 
    SWM = SpaceWeatherMonitor()
    SWD = SpaceWeatherData()
    FM = FileManager()
    AH = ActionHandler()
    P = Plotter()

    # SET PARAMETERS
    SWM.set_monitor_signal ( signal )
    SWM.set_trend_limits( 5, 90, 1 )
    FM.set_state_filepath( 'app/state/state.json' )
    FM.set_plot_filepath( 'app/plots/plot.png' )
    AH.set_plot_filepath( 'app/plots/plot.png' )
    P.set_height_width( 10, 12 )
    P.enable_warning_filter()

    # PROCESS DATA
    data_primary = SWD.get_data_primary()
    data_secondary = SWD.get_data_secondary()
    data = SWM.get_data( data_primary, data_secondary )
 
    if not data:
        return {}

    data_by_signal = SWD.parse_data_by_signal( data, signal )
    
    # GET STATE/ACTION FROM TREND/LIMITS
    trend_pass = SWM.check_trend( data_by_signal['values'] )
    level = SWM.get_level( data_by_signal['values'] )
    value = data_by_signal['values'][-1]
    current_state = SWM.get_state( value )
    previous_state = (FM.load_state())['state']
    action = SWM.get_action( current_state, previous_state, trend_pass )
    previous_action = SWM.state_to_action.get( previous_state, 'UNKNOWN' )

    # METADATA
    meta = {
        'action': action,
        'level': level,
        'value': value,
        'signal': signal,
        'created': data['created'] ,
        'source': data['source'],
        'state': current_state,
        'previous_action': previous_action
    }

    # EXECUTE ACTION
    payload = AH.execute_action( FM, P, meta, data_by_signal, signal )

    time = datetime.now().isoformat()

    print( """
    \n%s...CHECK_SPACE_WEATHER...ACTIONS:%s/%s|FLUX:%spfu|PASS?:%s
    """ % ( time, action, previous_action, value, trend_pass ) )

    return payload

##############################################
# GET ALL DATA (BOTH PRIMARY+SECONDARY)

def process_get_data( ):
    """Get both primary and secondary data."""

    SWD = SpaceWeatherData()

    data_primary = SWD.get_data_primary()
    data_secondary = SWD.get_data_secondary()
    payload = { 'primary': data_primary, 'secondary': data_secondary }

    return payload

##############################################
# GET DATA BY SPECIFIED SIGNAL (IF AVAILABLE)

def process_get_data_by_signal( signal ):
    """Get primary data filtered by specific signal."""

    SWD = SpaceWeatherData()
    
    data_primary = SWD.get_data_primary()
    if signal in data_primary['data'][0]:
        data_by_signal = SWD.parse_data_by_signal( data_primary, signal )
        payload = data_by_signal
    else:
        payload = {}

    return payload

##############################################
# RESET STATE JSON FILE (LOCAL)

def reset_state( ):
    """Reset state to 0."""
    FM = FileManager()
    FM.save_state( 0 )
    return {}