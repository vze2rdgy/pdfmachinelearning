#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/iclapadm/iclap")

from webstarter import startapp
app = startapp()
app.secret_key = 'esHorz2017'
application = app
