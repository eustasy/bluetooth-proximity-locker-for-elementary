#!/usr/bin/python

import sys
import os
import shutil
from optparse import OptionParser
import subprocess
import datetime
import time

DEVICEADDR = 'AA:BB:CC:DD:EE:FF'  # bluetooth device address
CHECKINTERVAL = 1  # device pinged at this interval (seconds) when screen is unlocked
CHECKREPEAT = 1  # device must be unreachable this many times to lock or unlock
#UNLOCKUSER = 'user'  # user to auto unlock at presence
mode = 'unlocked'

if __name__ == '__main__':
    while True:
        tries = 0
        while tries < CHECKREPEAT:
            TIMESTAMP = '{:%Y-%m-%d %H:%M:%S} Device '.format(datetime.datetime.now())
            process = subprocess.Popen(['sudo', '/usr/bin/l2ping', DEVICEADDR, '-t', '1', '-c', '1'], shell=False, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                print(TIMESTAMP + DEVICEADDR + ' Pinged OK')
                break
            print(TIMESTAMP + DEVICEADDR + ' Ping Error: Response Code: %d' % (process.returncode))
            time.sleep(1)
            tries = tries + 1

        if process.returncode == 0 and mode == 'locked':
            mode = 'unlocked'
            print('Device ' + mode + '.')
            # This _does_ unlock the session, but it remains on tty8 (lockscreen).
            # sudo loginctl unlock-sessions
            subprocess.Popen(['sudo', 'loginctl', 'unlock-sessions'], shell=False, stdout=subprocess.PIPE)
            # Switch to tty7 (mainscreen)
            # sudo chvt 7
            subprocess.Popen(['sudo', 'chvt', '7'], shell=False, stdout=subprocess.PIPE)
            #if UNLOCKUSER:
                # dm-tool switch-to-user UNLOCKUSER
                #subprocess.Popen(['dm-tool', 'switch-to-user', UNLOCKUSER], shell=False, stdout=subprocess.PIPE)

        if process.returncode == 1 and mode == 'unlocked':
            mode = 'locked'
            print('Device ' + mode + '.')
            # sudo loginctl lock-sessions
            #subprocess.Popen(['sudo', 'loginctl', 'lock-sessions'], shell=False, stdout=subprocess.PIPE)
            # loginctl has a delay on lock, but the proper tool (dm-tool) does not unlock
            # dm-tool lock
            subprocess.Popen(['dm-tool', 'lock'], shell=False, stdout=subprocess.PIPE)

        if mode == 'locked':
            time.sleep(CHECKINTERVAL)
        else:
            time.sleep(CHECKINTERVAL)
