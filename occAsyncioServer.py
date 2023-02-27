#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Uli Köhler"
__license__ = "CC0 1.0 Universal"

import asyncio
from colors import red
import serial_asyncio
import time

from occCore import *
from occAsyncioServer import *
from occSlip import *

SLIP_END = 0o300
SLIP_ESC = 0o333
SLIP_ESCEND = 0o334
SLIP_ESCESC = 0o335


class SLIPProtocol(asyncio.Protocol):
    def __init__(self):
        self.occ_response = ""

    def connection_made(self, transport):
        self.msg = bytes() # Message buffer
        self.transport = transport
        
        ##print('port opened', transport)
        transport.serial.rts = True  # You can manipulate Serial object via transport
        # Send "enter" to prompt output
        self.buf = b''

        # Handshake with Secure Element
        self.transport.serial.write(b'|b')

        # asyncio.ensure_future(self.send()) # from here i have to go forward

    '''async def send(self):
        time.sleep(0.3)

        msg = OSCMessage()
        msg.setAddress("/IHW/trnd")
        msg.append(64, 'i')

        slipEncoder = OccSlip()
        payload = slipEncoder.encodeToSLIP(msg.getBinary())
        payload = ''.join(map(str, payload))
        payload = payload.encode('utf-8')
        payload = payload.replace(b'192', b'\xc0')

        for b in payload:
            await asyncio.sleep(0.001)
            self.transport.serial.write(bytes([b]))
            print(f'Writer sent: {bytes([b])}')

        time.sleep(0.3)
        self.transport.close()'''

    def check_for_slip_message(self):
        # Identify end of message in data
        decoded = []
        last_char_is_esc = False
        for i in range(len(self.buf)):
            c = self.buf[i]
            if last_char_is_esc:
                # This character must be either
                # SLIP_ESCEND or SLIP_ESCESC
                if c == SLIP_ESCEND: # Literal END character
                    decoded.append(SLIP_END)
                elif c == SLIP_ESCESC: # Literal ESC character
                    decoded.append(SLIP_ESC)
                else:
                    # Ignore bad part of message
                    self.buf = self.buf[i+1:]
                    break
                last_char_is_esc = False # Reset state
            else: # last char was NOT ESC
                if c == 192: # END of message
                    # Remove current message from buffer
                    self.buf = self.buf[i+1:]
                    # Emit message
                    return bytes(decoded)
                elif c == SLIP_ESC:
                    # Handle escaped character next 
                    last_char_is_esc = True
                else: # Any other character
                    decoded.append(c)
        # No more bytes in buffer => no more message    
        return None

    def data_received(self, data):
        # Append new data to buffer
        self.buf += data
        while True:
            msg = self.check_for_slip_message()
            if msg is None:
                break # Need to wait for more data
            else: # msg is not None
                try:
                    self.occ_response = decodeOSC(msg)
                    print(self.occ_response)
                    #self.transport.close()
                except:
                    True

    def connection_lost(self, exc):
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')


    def resume_writing(self):
        print('resume writing')


