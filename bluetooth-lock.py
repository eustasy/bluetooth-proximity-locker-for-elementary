#!/usr/bin/python

import sys
import os
import shutil
from optparse import OptionParser
import subprocess
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
            process = subprocess.Popen(['sudo', '/usr/bin/l2ping', DEVICEADDR, '-t', '1', '-c', '1'], shell=False, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                print(DEVICEADDR + ' Pinged OK')
                break
            print(DEVICEADDR + ' Ping Error: Response Code: %d' % (process.returncode))
            time.sleep(1)
            tries = tries + 1

        if process.returncode == 0 and mode == 'locked':
            mode = 'unlocked'
            print(mode)
            # sudo loginctl unlock-sessions
            subprocess.Popen(['sudo', 'loginctl', 'unlock-sessions'], shell=False, stdout=subprocess.PIPE)
            #if UNLOCKUSER:
                # dm-tool switch-to-user UNLOCKUSER
                #subprocess.Popen(['dm-tool', 'switch-to-user', UNLOCKUSER], shell=False, stdout=subprocess.PIPE)

        if process.returncode == 1 and mode == 'unlocked':
            mode = 'locked'
            print(mode)
            # sudo loginctl lock-sessions
            subprocess.Popen(['sudo', 'loginctl', 'lock-sessions'], shell=False, stdout=subprocess.PIPE)
            # dm-tool lock
            #subprocess.Popen(['dm-tool', 'lock'], shell=False, stdout=subprocess.PIPE)

        time.sleep(CHECKINTERVAL)
