# !/usr/bin/env python
# -*- coding: utf-8 -*-

from Pubnub import Pubnub
from bottle import *
from marlight import Bulb

bulb = Bulb(ip='192.168.0.101', channel=2)

pubnub = Pubnub(
    "pub-c-d57a7240-b559-4586-81d6-b7c558286c94",  ## PUBLISH_KEY
    "sub-c-ba5e8552-1816-11e4-bddd-02ee2ddab7fe",  ## SUBSCRIBE_KEY
    "sec-c-YTRmZWQyZmQtMjBjZS00NWMzLTk0Y2MtNmFiYTQyOGU3YzY5",    ## SECRET_KEY
    False    ## SSL_ON?
)


@post('/battery')
def battery():
    lvl = request.POST['level']
    name = request.POST['device']
    msg = {}
    if name == 'HTC One X':
        msg['phone_battery'] = lvl
    elif name == 'SM-T320':
        msg['tablet_battery'] = lvl
    p = pubnub.publish(
        channel='averrin:smart',
        message=msg
    )
    return {"success": True, "pubnub": p}

@post('/wifi')
def wifi():
    network = request.POST['network']
    print('wifi: %s' % network)
    name = request.POST['device']
    msg = {}
    if name == 'HTC One X':
        msg['phone_network'] = network
        if network == "\"Averrin\"":
            bulb.all_on()

    p = pubnub.publish(
        channel='averrin:smart',
        message=msg
    )
    return {"success": True, "pubnub": p}


run(host='0.0.0.0', port=8888)