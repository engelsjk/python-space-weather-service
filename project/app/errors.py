"""
errors.py
Error class for app views responses.
"""

class GeneralError( Exception ):
    status_code = 400

    def __init__( self, message, status_code=None, payload=None ):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict( self ):
        rv = dict( self.payload or () )
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        return rv