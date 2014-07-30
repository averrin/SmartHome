# !/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from time import sleep

MODE_TIMER = (0x18, 0x00, 0x00, 0x00, 0x00, 0x09, 0x14, 0x55)
MODE_ALARM = (0x19, 0x00, 0x00, 0x09, 0x14, 0x55)


class Bulb():
    def __init__(self, ip='192.168.0.104', port=50000, channel=1):
        self.ip = ip
        self.port = port
        self.channel = channel
        self.delay = 0.2
        self.mode = 'normal'
        onoff = (
            ((0x08, 0x55), (0x09, 0x55)),
            ((0x0A, 0x55), (0x0B, 0x55)),
            ((0x0C, 0x55), (0x0D, 0x55)),
            ((0x0E, 0x55), (0x0F, 0x55))
        )
        self.commands = {
            'on': onoff[self.channel-1][0],
            'off': onoff[self.channel-1][1],
            'all_on': (0x01, 0x55),
            'all_off': (0x02, 0x55),
            'set_default_temp': (0x07, 0x55),
            'lighter': (0x03, 0x55),
            'rgb_lighter': (0x11, 0x55),
            'darker': (0x04, 0x55),
            'rgb_darker': (0x10, 0x55),
            'colder': (0x05, 0x55),
            'warmer': (0x06, 0x55)
        }
        self.modes = {
            'rgb': (0x12, 0x55),
            'night': (0x14, 0x55),
            'meeting': (0x15, 0x55),
            'reading': (0x16, 0x55),
            'mode': (0x17, 0x55),
            'sleep': (0x1A, 0x55)
        }

    def _sendMessage(self, dgramm):
        message = ''
        for c in dgramm:
            message += '%c' % c
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(message, "utf-8"), (self.ip, self.port))
        sleep(self.delay)
        sock.close()

    def set_color(self, color, flag=0x13):
        if color.startswith('#'):
            color = color[1:]
        r, g, b = color[:2], color[2:4], color[4:6]
        self._sendMessage([flag, int(r, 16), int(g, 16), int(b, 16), 0x55])

    def recreation(self, color):
        self.set_color(color, flag=0x1B)

    def set_mode(self, mode):
        self._sendMessage(self.modes[mode])
        self.mode = mode

    on = lambda self: self._sendMessage(self.commands['on'])
    off = lambda self: self._sendMessage(self.commands['off'])
    all_on = lambda self: self._sendMessage(self.commands['all_on'])
    all_off = lambda self: self._sendMessage(self.commands['all_off'])
    set_default_temp = lambda self: self._sendMessage(self.commands['set_default_temp'])
    lighter = lambda self: self._sendMessage(self.commands['rgb_lighter' if self.mode in ('rgb', 'recreation') else 'lighter'])
    darker = lambda self: self._sendMessage(self.commands['rgb_darker' if self.mode in ('rgb', 'recreation') else 'darker'])
    colder = lambda self: self._sendMessage(self.commands['colder'])
    warmer = lambda self: self._sendMessage(self.commands['warmer'])

# bulb = Bulb(ip='192.168.0.101', channel=2)
#
# bulb.all_off()
# bulb.all_on()
# # bulb.set_mode('rgb')
# # bulb.set_color('#00ffff')
# print(bulb.mode)
# sleep(1)
# for _ in range(10):
#     bulb.lighter()
#     sleep(0.1)