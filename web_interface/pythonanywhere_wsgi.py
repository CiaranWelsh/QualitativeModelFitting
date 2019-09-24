import sys
import os
# add your project directory to the sys.path
WD = os.path.dirname(os.path.dirname(__file__))
WEB_INTERFACE_DIR = os.path.join(WD, 'web_interface')
APP_DIR = os.path.join(WEB_INTERFACE_DIR, 'extended_pi3k_with_dash')
ASSETS_DIR = os.path.join(APP_DIR, 'assets')

for i in [WD, WEB_INTERFACE_DIR, APP_DIR, ASSETS_DIR]:
    if i not in sys.path:
        sys.path = [i] + sys.path

# need to pass the flask app as "application" for WSGI to work
# for a dash app, that is at app.server
# see https://plot.ly/dash/deployment
from web_interface.extended_pi3k_with_dash import app
application = app.server