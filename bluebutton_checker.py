# -*- coding: utf-8 -*-
import evdev

import os

# 送信フラグ
is_push_harvest = False

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
for device in devices:
    print (device.fn, device.name, device.phys)
bluebutton = evdev.InputDevice('/dev/input/event0')

filename = 'is_push'

while True :
    events = bluebutton.read_one()
    if events == None:
        continue
    events = bluebutton.read()
    event = next(events)
    
    if event.type == evdev.ecodes.EV_KEY:
        if evdev.util.categorize(event).keycode == 'KEY_ENTER': # is small button?
            print(evdev.util.categorize(event).keycode,'is push.')
            is_push_harvest = False

            if os.path.exists(filename):
                os.remove(filename)

        if evdev.util.categorize(event).keycode == 'KEY_VOLUMEUP': # is big button?
            print(evdev.util.categorize(event).keycode,'is push.')
            is_push_harvest = True
            
            if not os.path.exists(filename):
                f=open(filename,'w')
                f.close()