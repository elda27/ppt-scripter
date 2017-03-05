print('Invoked runserver.wsgi')

import sys
sys.path.append('./Source/')

import os
import www.server

import logging
# apacheのログに出すために必要
logging.basicConfig(stream = sys.stderr)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)
os.chdir('./www')
www.server.main(True)
