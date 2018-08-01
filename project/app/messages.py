"""
messages.py
Creates and sends email and HTTP messages.
"""

import requests
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage

from app import app

##############################################
# CREATE EMAIL HTML w/ IMAGES

def create_email( sender, recipients, meta, plot_name ):
    """Create event email (w/ plot) and returns MIME message."""

    action = meta['action'].upper()
    previous_action = meta['previous_action'].upper()
    value = meta['value']
    date = meta['created']
    source = meta['source']
    link = app.config['DATA_LINK']
    image = plot_name

    subject = 'Space Weather %s' % action.upper()
    body = """<p>
        Space Weather %s<br>
        Current Proton Flux >= 10 MeV @ %s pfu<br>""" % ( action, value)

    if action == 'INFO':
        body += """Recent %s event has passed!<br>""" % ( previous_action )

    body += """
        </p>
        <img src="cid:%s" width="700"><br>
        <p>
        Data File Created at %s<br>
        Detected by NOAA's %s Satellite<br>
        For more information: %s</br>
        </p>""" % ( image, date, source, link )

    ###

    msg = MIMEMultipart( 'alternative' )
    msg['From'] = sender
    msg['To'] = ', '.join( recipients )
    msg['Subject'] = subject

    msgText = MIMEText( body,'html' )  
    msg.attach( msgText )   

    fp = open( plot_name, 'rb' )                                                    
    img = MIMEImage( fp.read() )
    fp.close()
    img.add_header( 'Content-ID', '<{}>'.format( plot_name ) )
    msg.attach( img )

    return msg

##############################################
# SEND EMAIL VIA SMTP

def send_email( meta, plot_name ):
    """Send email via external SMTP server."""

    sender  = app.config['MESSAGE_SENDER']
    recipients = app.config['MESSAGE_RECIPIENTS']

    host = app.config['SMTP_HOST']
    port = app.config['SMTP_PORT']
    username = app.config['SMTP_USERNAME']
    password = app.config['SMTP_PASSWORD']

    email = create_email( 
        sender, recipients, 
        meta, 
        plot_name 
    )

    try:  
        server = smtplib.SMTP( host, port )
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login( username, password )
        server.sendmail( sender, recipients, email.as_string() )
        server.close()
    except:
        print("\nWARNING: There was an error trying to send an email alert! Please check all SMTP and email parameters in config.json!")
   
##############################################
# CREATE ALERT MESSAGE (JSON)

def create_alert( meta ):
    """Create alert message for an HTTP/JSON payload."""

    alert_text = """Space weather %s: >=10 MeV proton flux currently at %s pfu!
    """ % ( int( meta['level']['tens'] ), meta['value'] )

    link = app.config['DATA_LINK']

    msg = {
        "alert_text": alert_text,
        "level": meta['level']['tens'],
        "value": meta['value'],
        "link": link
    }

    return msg

##############################################
# SEND ALERT MESSAGE (JSON) TO USER-DEFINED URL (HTTP POST)

def send_alert( meta ):
    """Send HTTP/JSON alert message to URL."""

    msg = create_alert( meta )
    url = app.config['MESSAGE_URL']
    try:
        r = requests.post( url, json=msg )
        t = json.loads( r.text )
        print( "\nNotification Message (%s) Sent via HTTP POST!" % meta['action'] )
        print( "\nHTTP POST RESPONSE: %s" % t )
        return t
    except requests.exceptions.RequestException as e:
        return {}