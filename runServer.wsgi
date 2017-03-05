import sys
sys.path.append('./Source/')

import os
import www.server

import logging
# apacheのログに出すために必要
logging.basicConfig(stream = sys.stderr)

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
	os.chdir('./www')
	www.server.main()
