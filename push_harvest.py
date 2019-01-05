# -*- coding: utf-8 -*-

from gps3 import gps3
import json
import urllib.request

import os
import time
import configparser
 
# debug用
from pprint import pprint
 
ini = configparser.ConfigParser()

# iniファイル存在チェック
INI_PATH = os.path.dirname(__file__)+'/config.ini'
if not os.path.exists(INI_PATH):
    print('ERR : "./config.ini" is not found.')
    sys.exit(1)

ini.read(INI_PATH, 'UTF-8')

# import logging
# logging.config.fileConfig("logging_debug.conf")
# logger = logging.getLogger()

# soracom Inventoryキー
## config.iniを参照
DEVICE_ID = ini.get('soracom', 'device_id')
SERCRET_KEY = ini.get('soracom', 'sercret_key')

if DEVICE_ID == '' or SERCRET_KEY == '':
    print('ERR : "device key" or "sercret key" is not found. ')
    sys.exit(1)
print('soracom inventory keys is ')
print('    '+ini.get('soracom', 'device_id'))
print('    '+ini.get('soracom', 'sercret_key'))

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
        # logger.info(filename +'is not exists')
        data_stream.unpack(new_data)
        
        # Bluttoothボタンの大小どちらか押したかによって生死が変わる
        if os.path.exists(filename):
            data_stream.TPV['is_alive'] = 1
        else:
            data_stream.TPV['is_alive'] = 0

        print("~~~~~~~~~~~")
        print('is_alive : ', data_stream.TPV['is_alive'])
        print('time : ', data_stream.TPV['time'])
        print('lat : ', data_stream.TPV['lat'])
        print('lon : ', data_stream.TPV['lon'])
        print('alt : ', data_stream.TPV['alt'])
        print('speed : ', data_stream.TPV['speed'])

        # if data_stream.TPV['time'] == 'n/a' \
        #     or data_stream.TPV['lat'] == 'n/a' \
        #     or data_stream.TPV['lon'] == 'n/a' \
        #     or data_stream.TPV['alt'] == 'n/a' \
        #     or data_stream.TPV['speed'] == 'n/a' :
        #     # ごみなので捨てる
        #     # logger.info('gps data is null')    
        #     continue
  
        url = 'https://api.soracom.io/v1/devices/'+DEVICE_ID+'/publish'
        data = {
            'is_alive' : data_stream.TPV['is_alive'],
            'time' : data_stream.TPV['time'],
            'lat' : data_stream.TPV['lat'],
            'lon' : data_stream.TPV['lon'],
            'alt' : data_stream.TPV['alt'],
            'speed' : data_stream.TPV['speed'],
        }
        headers = {
            'x-device-secret': SERCRET_KEY,
        }
        pprint(json.dumps(data).encode())

        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = res.read()
            time.sleep(1)
        # logger.info('gps data is pushed')
        # logger.debug(req)