"""
monitors.py
Defines logic for space weather monitoring (actions / states).
"""

from app import app
import math

##############################################
# SpaceWeatherMonitor

class SpaceWeatherMonitor:

    state_to_action = {
        0: 'NONE',
        1: 'WARNING',
        2: 'ALERT',
        3: 'CRITICAL'
    }

    interval_min = 5    # Time step interval of data points (min)
    trend_duration_min = 90      # Length of trend to check for monitoring.
    trend_limit = 1     # Trend limit of proton flux (pfu)

    # Set proton flux limit ranges (pfu)
    limits = {
        0: 1,
        1: 10,
        2: 100
    }

    def __init__( self ):
        pass 

    def set_monitor_signal( self, signal ):
        self.signal = signal or ''

    def set_trend_limits( self, interval_min, trend_duration_min, trend_limit ):
        self.interval_min = interval_min
        self.trend_duration_min = trend_duration_min
        self.trend_limit = trend_limit
    
    def get_data( self, data_1, data_2 ):
        """Select data by availability of primary vs secondary sources."""
        if 'data' in data_1:
            data = data_1 if len( data_1['data'] ) != 0 else {}
        elif 'data' in data_2:
            data = data_2 if len( data_2['data'] ) != 0 else {}
        else:
            data = {}
        return data

    def check_trend( self, data ):
        """Check trend of data (i.e. if data < limit for duration)."""
        trend_range = math.floor( self.trend_duration_min / self.interval_min )
        trend_data = data[-trend_range:]
        trend_pass = all( d < self.trend_duration_min for d in trend_data )
        return trend_pass

    def get_level_exp( self, value ):
        """Calculate log10 level of value."""
        if value > 0:
            level_exp = int( math.floor( math.log10( value ) ) )
        else: 
            level_exp = -1
        return level_exp

    def get_level_tens( self, value ):
        """Calculate 10^value."""
        level_tens = int( math.pow( 10, value ) )
        return level_tens

    def get_level( self, data ):
        """Return level (tens and exp)."""
        level = {'exp': None, 'tens': None }
        value = data[-1]
        level_exp = self.get_level_exp( value )
        level_tens = self.get_level_tens( level_exp )
        level['exp'] = level_exp
        level['tens'] = level_tens
        return level

    def get_state( self, value ):
        """Get state based on value/limit checks."""
        if value <= self.limits[1]:
            state = 0
        elif self.limits[1] < value <= self.limits[2]:
            state = 1
        elif self.limits[2] < value <= self.limits[3]:
            state = 2
        elif self.limits[3] > 100:
            state = 3
        else:
            state = -1

        return state

    def get_action( self, current_state, previous_state, trend_pass ):
        """Get action by comparing current/previous states and trend."""
        if current_state > previous_state:
            action = self.state_to_action.get( current_state, 'NONE' )
        elif previous_state != 0 and current_state == 0 and trend_pass:
            action = 'INFO'
        else:
            action = 'NONE'

        return action

        






########################################



