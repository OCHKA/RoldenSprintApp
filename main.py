# Runner for buildozer packaged app

import os
from runpy import run_module

os.environ['AIOCOAP_CLIENT_TRANSPORT'] = 'simple6'  # Android doesn't work with udp6
run_module('roldensprint', run_name='__main__', alter_sys=True)
