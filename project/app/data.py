"""
data.py
Loads, parses and filters data.
"""

import requests
import json 
from datetime import datetime

from app import app

##############################################
# SpaceWeatherData

class SpaceWeatherData:

    timeout = 10    # Timeout for external data requests

    # Data column names for parsing raw txt file column headers
    keys = [
        'YR','MO','DA','HHMM','MJD','SOD',
        'P1','P5','P10','P50','P100',
        'E0p8','E2p0','E4p0'
    ]
    
    def __init__( self ):
        pass

    def get_data_primary( self ):
        """Get data (primary source) from URL."""
        url = app.config['DATA_PRIMARY_URL']
        try:
            d = requests.get(url, timeout=self.timeout ).text
            j = self.parse_raw_data( d )
            return j
        except requests.exceptions.RequestException:
            return {}

    def get_data_secondary( self ):
        """Get data (secondary source) from URL."""
        url = app.config['DATA_SECONDARY_URL']
        try:
            d = requests.get(url, timeout=self.timeout ).text
            j = self.parse_raw_data( d )
            return j
        except requests.exceptions.RequestException:
            return {}

    def parse_raw_data( self, data ):
        """Parse raw data to turn .txt into .json"""

        output = {
            'filename': '',
            'created': '',
            'source': '',
            'data':[]
        }

        """Set of parser functions for line-by-line parsing of .txt data file"""
        def parse_filename( line ):
            return [0, 'filename', line.split( ":Data_list: ",1 )[1]]
        def parse_created( line ):
            return [0, 'created', line.split( ":Created: ",1 )[1]]
        def parse_source( line ):
            return [0, 'source', line.split( "# Source: ",1 )[1]]
        def parse_location( line ):
            return [0, 'location', line.split( "# Location: ",1 )[1]]
        def parse_data_start( line ):
            return parse_data( line )
        def parse_data( line ):
            return [1, '', dict(zip(self.keys,d.split()))]
        def skip( line ):
            return [-1, '', '']

        """Switcher dictionary of parser functions by line index."""
        switcher = {
            1: parse_filename,
            2: parse_created,
            17: parse_source,
            18: parse_location,
            27: parse_data_start
        }

        """Line-by-line loop of text parsing."""
        try:
            ii = 1
            data_check = 0
            for d in data.splitlines():
                func = switcher.get( ii, lambda x: parse_data( x ) if data_check==1 else skip( x ) )
                o = func( d )
                data_check = o[0]
                ii += 1
                if data_check == 1:
                    output['data'].append( o[2] )
                elif data_check == 0:
                    output[o[1]] = o[2]
                elif data_check == -1:
                    continue
        except:
            pass

        return output

    def parse_timestamp( self, d ):
        """Parser for txt file timestamp format."""
        ts = '-'.join( [d['YR'], d['MO'], d['DA']] ) + ' ' + d['HHMM']
        t = datetime.strptime( ts, '%Y-%m-%d %H%M' )
        return t.isoformat()

    def parse_data_by_signal( self, data, signal ):
        """Parser for filtering data by specific signal."""
        output = { 'name': signal, 'values': [], 'time': [] }

        try:
            x = [float( d[signal] ) for d in data['data']]
            t = [self.parse_timestamp( d ) for d in data['data']]
            output['values'] = x
            output['time'] = t
        except:
            pass
        
        return output