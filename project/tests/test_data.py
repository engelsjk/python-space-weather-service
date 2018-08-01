"""
test_data.py
A series of testing functions for the 'data' module, and 
specifically the SpaceWeatherData class and its methods.
"""

import sys,os
import requests
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from app import data
from app import app

SWD = data.SpaceWeatherData()

def test_data_primary():
    d = SWD.get_data_primary()
    assert type( d ) is dict
    assert 'data' in d

def test_data_secondary():
    d = SWD.get_data_secondary()
    assert type( d ) is dict
    assert 'data' in d

def test_parse_raw_data():
    url = app.config['DATA_SECONDARY_URL']
    rd = requests.get(url).text
    d = SWD.parse_raw_data( rd )
    assert type( d ) is dict
    assert 'filename' in d
    assert 'created' in d
    assert 'source' in d
    assert 'data' in d

def test_parse_data_by_signal_good():
    d = SWD.get_data_primary()
    pd = SWD.parse_data_by_signal( d, 'P10' )
    assert 'name' in pd
    assert 'values' in pd
    assert 'time' in pd

def test_parse_data_by_signal_bad():
    d = SWD.get_data_primary()
    pd = SWD.parse_data_by_signal( d, 'XXX' )
    assert 'name' in pd
    assert 'values' in pd
    assert 'time' in pd