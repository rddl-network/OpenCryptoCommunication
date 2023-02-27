import time

import asyncio
import serial_asyncio

from occAsyncioServer import *
from occSlip import *

class OutputProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        transport.write(b'Hello, World!\n')  # Write serial data via transport
        time.sleep(0.8)

        msg = OSCMessage()
        msg.setAddress("/IHW/mnemonic")
        msg.append(64, 'i')

        print(msg)

        slipEncoder = OccSlip()
        payload = slipEncoder.encodeToSLIP(msg.getBinary())

        payload = ''.join(map(str, payload))
        payload = payload.encode('utf-8')
        payload = payload.replace(b'192', b'\xc0')

        print(payload)

        transport.serial.write(payload)

    def data_received(self, data):
        print('data received', repr(data))
        #if b'\n' in data:
        if b'\xc0' in data:
            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')

loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, OutputProtocol, '/dev/ttyUSB0', baudrate=115200)
transport, protocol = loop.run_until_complete(coro)



loop.run_forever()
loop.close()