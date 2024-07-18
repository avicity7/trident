#!/usr/bin/env python
import os
import time

#turn projector on, change input source etc
while True:
    os.system('irsend SEND_ONCE epson Power')
    time.sleep(1)
