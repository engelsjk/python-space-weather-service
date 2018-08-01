"""
action.py
Defines and executes actions for the SpaceWeatherMonitor.
"""

from app import app

import app.messages as messages

##############################################
# ActionHandler

class ActionHandler:

    meta = {}   # Meta data on current status, created in 'processes'.
    data = {}   # Signal data from 'processes'.
    signal = '' # Selected signal related to data.
    FM = {}     # FileManager 
    P = {}      # Plotter

    def __init__( self ):
        """Initalize class by loading action handlers."""
        self.set_action_handlers()

    def set_plot_filepath( self, plot_filepath ):
        """Set the filepath where the plot image will be saved."""
        self.plot_filepath = plot_filepath or ''

    def set_action_handlers( self ):
        """Define set of actions/handlers; 
        must match state_to_actions defined in SpaceWeatherMonitors!"""
        self.action_handlers = {
            'NONE': self.handle_none,
            'WARNING': self.handle_warning,
            'ALERT': self.handle_alert,
            'CRITICAL': self.handle_critical,
            'INFO': self.handle_info
        }

    def create_plot( self ):
        """Create and save plot from Plotter."""
        plot = self.P.create_plot( self.data, self.meta )
        self.FM.save_plot( plot, self.P.height, self.P.width )

    def handle_none( self ):
        """NONE: Returns meta data."""
        return {'m': self.meta, 'a': ''}

    def handle_warning( self ):
        """WARNING: Creates plot, sends HTTP POST alert + email and returns meta/alert data."""
        alert = messages.send_alert( self.meta )
        self.create_plot()
        messages.send_email( self.meta, self.plot_filepath )
        return {'m': self.meta, 'a': alert}

    def handle_alert( self ):
        """ALERT: Creates plot, sends HTTP POST alert + email and returns meta/alert data."""
        alert = messages.send_alert( self.meta )
        self.create_plot()
        messages.send_email( self.meta, self.plot_filepath )
        return {'m': self.meta, 'a': alert}
        
    def handle_critical( self ):
        """CRTICAL: Creates plot, sends HTTP POST alert + email and returns meta/alert data."""
        alert = messages.send_alert( self.meta )
        self.create_plot()
        messages.send_email( self.meta, self.plot_filepath )
        return {'m': self.meta, 'a': alert}

    def handle_info( self ):
        """INFO: Creates plot, sends HTTP POST alert + email and returns meta/alert data."""
        alert = messages.send_alert( self.meta )
        self.create_plot()
        messages.send_email( self.meta, self.plot_filepath )
        return {'m': self.meta, 'a': alert}

    def handle_default( self ):
        """DEFAULT: Returns meta data."""
        return {'m': self.meta, 'a': ''}

    def execute_action( self, FM, P, meta, data, signal ):
        """Selects action function from meta data, executes action function, 
        updates state and returns action handler output."""
        self.meta = meta
        self.data = data
        self.signal = signal
        self.FM = FM
        self.P = P
        
        action_func = self.action_handlers.get( self.meta['action'], lambda: handle_default )
        handler_output = action_func()
        self.update_state( self.meta['action'], self.meta['state'] )
        return handler_output

    def update_state( self, action, state ):
        """Updates the state file based on the current action."""
        if action == 'NONE':
            pass 
        elif action == 'INFO':
            self.FM.save_state( 0 )
        else:
            self.FM.save_state( state )

    
