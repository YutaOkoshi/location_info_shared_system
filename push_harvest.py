# -*- coding: utf-8 -*-

from gps3 import gps3
import json
import urllib.request

import os
import time
# import logging

# logging.config.fileConfig("logging_debug.conf")

# logger = logging.getLogger()

# soracom Inventoryキー
DEVICE_ID = 'デバイスキー'
SERCRET_KEY = 'セキュリティーキー'

# GPS諸々設定
gps_socket = gps3.GPSDSocket()
data_stream = gps3.DataStream()
gps_socket.connect()
gps_socket.watch()

filename = 'is_push'
# logger.info('push_harvest 2 is start')

for new_data in gps_socket:

    # logger.debug('get for gps data')
    if new_data:
        if os.path.exists(filename):
            # logger.info(filename +'is exists')
            data_stream.unpack(new_data)
            print('is_alive : 1')
            print('time : ', data_stream.TPV['time'])
            print('lat : ', data_stream.TPV['lat'])
            print('lon : ', data_stream.TPV['lon'])
            print('alt : ', data_stream.TPV['alt'])
            print('speed : ', data_stream.TPV['speed'])
            
            if data_stream.TPV['time'] == 'n/a' \
                or data_stream.TPV['lat'] == 'n/a' \
                or data_stream.TPV['lon'] == 'n/a' \
                or data_stream.TPV['alt'] == 'n/a' \
                or data_stream.TPV['speed'] == 'n/a' :
                # ごみなので捨てる
                # logger.info('gps data is null')
                
                continue
            
            url = 'https://api.soracom.io/v1/devices/'+DEVICE_ID+'/publish'
            data = {
                'is_alive' : 1,
                'time' : data_stream.TPV['time'],
                'lat' : data_stream.TPV['lat'],
                'lon' : data_stream.TPV['lon'],
                'alt' : data_stream.TPV['alt'],
                'speed' : data_stream.TPV['speed'],
            }
            headers = {
                'x-device-secret': SERCRET_KEY,
            }

            req = urllib.request.Request(url, json.dumps(data).encode(), headers)
            with urllib.request.urlopen(req) as res:
                body = res.read()
                time.sleep(1)
            # logger.info('gps data is pushed')
            # logger.debug(req)

        else:
            # logger.info(filename +'is not exists')
            data_stream.unpack(new_data)
            print('is_alive : 0')
            print('time : ', data_stream.TPV['time'])
            print('lat : ', data_stream.TPV['lat'])
            print('lon : ', data_stream.TPV['lon'])
            print('alt : ', data_stream.TPV['alt'])
            print('speed : ', data_stream.TPV['speed'])
            
            if data_stream.TPV['time'] == 'n/a' \
                or data_stream.TPV['lat'] == 'n/a' \
                or data_stream.TPV['lon'] == 'n/a' \
                or data_stream.TPV['alt'] == 'n/a' \
                or data_stream.TPV['speed'] == 'n/a' :
                # ごみなので捨てる
                # logger.info('gps data is null')
                
                continue  
            
            url = 'https://api.soracom.io/v1/devices/'+DEVICE_ID+'/publish'
            data = {
                'is_alive' : 0,
                'time' : 'n/a', # data_stream.TPV['time'], 
                'lat' : 'n/a', # data_stream.TPV['lat'], 
                'lon' : 'n/a', # data_stream.TPV['lon'], 
                'alt' : 'n/a', # data_stream.TPV['alt'], 
                'speed' : 'n/a', # data_stream.TPV['speed'], 
            }
            headers = {
                'x-device-secret': SERCRET_KEY,
            }

            req = urllib.request.Request(url, json.dumps(data).encode(), headers)
            with urllib.request.urlopen(req) as res:
                body = res.read()
                time.sleep(1)
            # logger.info('gps data is pushed')
            # logger.debug(req)
