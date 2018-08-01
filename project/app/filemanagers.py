"""
filemanagers.py
Save and load files (state, plot and data).
"""

import json
from datetime import datetime

from app import app

##############################################
# FileManager

class FileManager:

    state_filepath = 'app/state/state.json'
    plot_filepath = 'app/plots/plot.png'

    def set_state_filepath( self, state_filepath ):
        self.state_filepath = state_filepath

    def set_plot_filepath( self, plot_filepath ):
        self.plot_filepath = plot_filepath

    def load_data( self ):
        with open( self.date_filepath ) as f:
            data = json.load( f )
        return data

    def save_data( self, data ):
        with open( self.date_filepath, 'w' ) as f:
            json.dump( data, f )
            
    def load_state( self ):
        with open( self.state_filepath ) as f:
            state = json.load(f)
        return state

    def save_state( self, state ):
        """Save current state and time to JSON file."""
        time = datetime.now().isoformat()
        state_o = {
            "state": state,
            "time": time
        }
        with open( self.state_filepath, 'w' ) as f:
            json.dump( state_o, f )

    def save_plot( self, plot, height, width ):
        try:
            plot.save( self.plot_filepath, height = height, width = width, dpi = 100 )
        except:
            pass

    def get_plot_filepath( self ):
        return self.plot_filepath