import sys
sys.path.append('./Source/')

import os
import www.server

if __name__ == '__main__':
	os.chdir('./www')
	www.server.main()
