"""
test_monitors.py
A series of testing functions for the 'monitors' module, and
specifically the SpaceWeatherMonitor class and its methods.
"""

import sys,os
import requests
import numpy as np
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from app import monitors
from app import data
from app import app

SWM = monitors.SpaceWeatherMonitor()
SWD = data.SpaceWeatherData()

def test_data_good():
    d1 = SWD.get_data_primary()
    d2 = SWD.get_data_secondary()
    d = SWM.get_data( d1, d2 )
    assert type( d ) is dict

def test_data_bad():
    d = SWM.get_data( {}, {} )
    assert type( d ) is dict

def test_check_trend():
    d = np.random.uniform(low=0, high=13.3, size=(50,))
    t = SWM.check_trend( d )
    assert type(t) is bool

def test_level_exp():
    le = SWM.get_level_exp( -1 )
    assert type(le) is int

def test_level_tens():
    lt = SWM.get_level_tens( -1 )
    assert type(lt) is int

def test_state():
    s = SWM.get_state( -1 )
    assert type(s) is int

def test_action():
    a = SWM.get_action( 0, 3, True )
    assert type(a) is str
    a = SWM.get_action( 0, 3, False )
    assert type(a) is str
    a = SWM.get_action( 3, 0, True )
    assert type(a) is str
    a = SWM.get_action( 3, 0, True )
    assert type(a) is str
    a = SWM.get_action( -1, -1, True )
    assert type(a) is str